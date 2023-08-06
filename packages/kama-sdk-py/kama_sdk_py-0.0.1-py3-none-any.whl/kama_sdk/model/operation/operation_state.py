from datetime import datetime
from typing import List, Optional, Dict

from kama_sdk.core.core import utils
from kama_sdk.model.operation.step_state import StepState


class OperationState:
  def __init__(self, uuid: str, operation_id: str):
    self.uuid: str = uuid
    self.op_id: str = operation_id
    self.step_states: List[StepState] = []
    self.status = 'running'
    self.preflight_telem = None

  def notify_preflight_performed(self, telem):
    self.preflight_telem = telem

  def notify_ended(self, status):
    self.status = status

  def gen_event_telem(self) -> Dict:
    return dict(
      _id=self.uuid,
      status=self.status,
      type='operation_outcome',
      name=self.op_id,
      occurred_at=str(datetime.now())
    )

  def find_step_state(self, step) -> StepState:
    matcher = lambda ss: ss.step_sig == step.sig()
    return next(filter(matcher, self.step_states), None)

  def gen_step_state(self, step, keep=True) -> StepState:
    self.del_step_state(step)
    new_ss = StepState(step.sig(), self)
    if keep:
      self.step_states.append(new_ss)
    return new_ss

  def del_step_state(self, step):
    matcher = lambda ss: not ss.step_sig == step.sig()
    self.step_states = list(filter(matcher, self.step_states))

  def all_assigns(self) -> Dict:
    merged = {}
    for step_state in self.step_states:
      merged = {**merged, **step_state.all_assigns()}
    return merged

  def gen_sub_map(self):
    assigns = self.all_assigns()
    keyed = utils.dict2keyed(assigns)
    return {f"$var/{k}": v for k, v in keyed}

  @classmethod
  def find(cls, ost_id: Optional[str]) -> 'OperationState':
    """
    Finds the OperationState with the marching osr id.
    :param ost_id: id to match by.
    :return: OperationState or None
    """
    matcher = lambda op_state: op_state.uuid == ost_id
    return next(filter(matcher, operation_states), None)

  @classmethod
  def gen(cls, operation_id: str) -> str:
    uuid = utils.rand_str(string_len=10)
    operation_states.append(OperationState(uuid, operation_id))
    return uuid

  @classmethod
  def delete_if_exists(cls, ost_id: Optional[str]) -> Optional['OperationState']:
    """
    Deletes the OperationState if one with the given osr id exists.
    :param ost_id: id used to locate the OperationState.
    :return: deleted instance of the OperationState if found, else None.
    """
    tuples = enumerate(operation_states)
    index = next((i for i, ops in tuples if ops.uuid == ost_id), None)
    return operation_states.pop(index) if index else None

  @classmethod
  def clear_list(cls):
    operation_states.clear()

  @classmethod
  def prune(cls):
    while cls.find(None):
      cls.delete_if_exists(None)


operation_states: List[OperationState] = []
