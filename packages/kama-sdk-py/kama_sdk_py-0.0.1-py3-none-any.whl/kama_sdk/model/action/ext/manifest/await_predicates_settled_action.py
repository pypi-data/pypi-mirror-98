import time
from typing import List

from werkzeug.utils import cached_property

from kama_sdk.core.core import consts
from kama_sdk.model.action.base.action import Action, FatalActionError
from kama_sdk.model.action.base.multi_action import MultiAction
from kama_sdk.model.operation.predicate_statuses_computer import PredicateStatusesComputer
from kama_sdk.model.supplier.predicate.predicate import Predicate


class AwaitPredicatesSettledAction(MultiAction):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._predicates_hack: List[Predicate] = []
    self._sub_actions_hack: List[Action] = []

  @cached_property
  def predicates(self) -> List[Predicate]:
    return self.inflate_children(
      Predicate,
      prop=PREDICATES_KEY,
      resolve_kod=False
    )

  @cached_property
  def timeout_seconds(self) -> int:
    return self.get_prop(TIMEOUT_SECONDS_KEY, 180)

  def final_sub_actions(self) -> List[Action]:
    return self._sub_actions_hack

  def perform(self, **kwargs) -> None:
    computer = PredicateStatusesComputer(self.predicates)

    optimists = computer.optimist_predicates
    self._sub_actions_hack = list(map(self.pred2action, optimists))

    start_ts = time.time()
    did_time_out = True

    while time.time() - start_ts < self.timeout_seconds:
      computer.perform_iteration()
      self.update_actions(computer)
      self.raise_for_negative_outcomes(computer)

      if computer.did_finish():
        did_time_out = False
        break
      else:
        time.sleep(2)

    raise_for_timeout(did_time_out)

  def find_action_by_pred(self, predicate_id: str) -> Action:
    finder = lambda action: action.config['predicate_id'] == predicate_id
    return next(filter(finder, self.final_sub_actions()))

  def update_actions(self, computer: PredicateStatusesComputer):
    for predicate in computer.optimist_predicates:
      evaluation = computer.find_eval(predicate.id())
      action = self.find_action_by_pred(predicate.id())
      action.set_status(consts.pos if evaluation['met'] else consts.rng)

  def pred2action(self, predicate: Predicate) -> Action:
    action = Action(dict(
      id=predicate.id(),
      title=predicate.title,
      info=predicate.info,
      predicate_id=predicate.id()
    ))
    action.parent = self
    return action

  @staticmethod
  def raise_for_negative_outcomes(computer: PredicateStatusesComputer):
    if computer.did_fail():
      predicate = computer.culprit_predicate()
      raise FatalActionError(
        type='predicate_settle_negative',
        resource=predicate.culprit_res_signature(),
        reason=predicate.reason,
        extras=predicate.error_extras()
      )


def raise_for_timeout(timed_out: bool):
  if timed_out:
    raise FatalActionError(
      type='predicate_settle_timeout',
      reason='Time'
    )


PREDICATES_KEY = 'predicates'
TIMEOUT_SECONDS_KEY = 'timeout_seconds'
