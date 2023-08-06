from typing import List, Dict, Optional, Union

from werkzeug.utils import cached_property

from kama_sdk.core.core import job_client, utils, consts
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import CommitOutcome, PredEval
from kama_sdk.model.base.model import Model
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.operation.field import Field
from kama_sdk.model.operation.operation_state import OperationState
from kama_sdk.model.operation.step_state import StepState

TOS = OperationState
TSS = StepState
TOOS = Optional[OperationState]
TCO = CommitOutcome


class Step(Model):

  @cached_property
  def reassignment_descs(self):
    return self.get_prop('reassignments', [])

  @cached_property
  def commit_strategy(self) -> Union[str, Dict]:
    return self.get_prop('commit_strategy', 'prepend-action')

  def sig(self) -> str:
    parent_id = self.parent.id() if self.parent else 'orphan'
    return f"{parent_id}::{self.id()}"

  def runs_action(self) -> bool:
    return bool(self.config.get(ACTION_KEY))

  def next_step_id(self, op_state: TOS) -> Optional[str]:
    self.patch(gen_downstream_patches(op_state, {}))
    return self.get_prop(NEXT_STEP_KEY)

  def validate_field(self, field_id: str, value: str, op_state: TOS) -> PredEval:
    return self.inflate_list_child(
      Field,
      prop=FIELDS_KEY,
      id=field_id,
      patches=gen_downstream_patches(op_state, {field_id: value})
    ).variable.validate(value)

  def visible_fields(self, assignments, op_state: TOS) -> List[Field]:
    fields = self.inflate_children(
      Field,
      prop=FIELDS_KEY,
      patches=gen_downstream_patches(op_state, assignments)
    )
    return [f for f in fields if f.compute_visibility()]

  def state_recall_descriptors(self, target: str):
    predicate = lambda d: d.get('to', consts.TARGET_STANDARD) == target
    return filter(predicate, self.reassignment_descs)

  def run(self, assigns: Dict, state: StepState) -> Optional[str]:
    buckets = self.partition_vars(assigns, state.parent_op)
    state.notify_vars_assigned(buckets)

    new_prefs = buckets[consts.TARGET_PREFS]
    if new_prefs:
      config_man.patch_prefs(new_prefs)

    job_id = None
    if self.runs_action():
      patched_action_config = self.gen_action_config(state.parent_op, buckets)
      if patched_action_config:
        job_id = job_client.enqueue_action(patched_action_config, **buckets)

    return job_id

  def gen_action_config(self, op_state: OperationState, buckets) -> Optional[Dict]:
    """
    In case the action has dynamic parts to it , we must resolve it
    before it runs in a different process (no shared memory). Also merges in
    event-telem config. Omits the unmarshalable 'context' of the config.
    @param op_state: step state that IFTT might use to make resolution
    @param buckets: value buckets eg chart, inline, state
    @return: un-IFTT'ed config dict for the action
    """
    values_patch = {}
    resolved_action = self.inflate_child(
      Action,
      prop=ACTION_KEY,
      patches=values_patch,
      safely=True
    )

    if resolved_action:
      return dict(
        **resolved_action.serialize(),
        **gen_downstream_patches(op_state, {}),
        commit={
          consts.TARGET_STANDARD: buckets[consts.TARGET_STANDARD],
          consts.TARGET_INLIN: buckets[consts.TARGET_INLIN]
        }
      )
    else:
      return None

  def partition_vars(self, inputs: Dict, op_state: TOS) -> Dict:
    self.patch(gen_downstream_patches(op_state, inputs))
    default_commit = self._partition_vars_by_field(inputs, op_state)
    self.patch(dict(commit=default_commit))
    commit_override = self.resolve_prop('commit_override', depth=100)
    return sanitize2(commit_override, default_commit)

  def _partition_vars_by_field(self, inputs: Dict, op_state: TOS) -> Dict:
    fields = self.visible_fields(inputs, op_state)
    types = consts.TARGET_TYPES
    return {t: filter_inputs_by_type(fields, inputs, t) for t in types}


def gen_downstream_patches(op_state: OperationState, user_input: Dict):
  return dict(
    op_state=op_state.all_assigns(),
    inputs=user_input
  )


def sanitize2(overrides: Dict, defaults: Dict) -> Dict:
  output = {}
  for key, default in defaults.items():
    override = (overrides or {}).get(key)
    if override == {}:
      final_dict = {}
    elif override is None:
      final_dict = default
    else:
      final_dict = override
    output[key] = utils.flat2deep(final_dict)
  return output


def filter_inputs_by_type(fields: List[Field], inputs: Dict, _type: str):
  flat_inputs = utils.deep2flat(inputs)

  def find_field(_id):
    return next(filter(lambda f: f.id() == _id, fields), None)

  gate = lambda k: find_field(k) and find_field(k).target == _type
  filtered_flat = {k: v for (k, v) in flat_inputs.items() if gate(k)}
  return utils.flat2deep(filtered_flat)


ACTION_KEY = 'action'
NEXT_STEP_KEY = 'next'
FIELDS_KEY = 'fields'
