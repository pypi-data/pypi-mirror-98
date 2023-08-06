from typing import List

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import KoD
from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.action.base.action import Action, FatalActionError, ActionError
from kama_sdk.model.action.base.multi_action import MultiAction
from kama_sdk.model.supplier.predicate.predicate import Predicate

class RunPredicateAction(Action):

  def id(self) -> str:
    from_super = super().id()
    return from_super or self.predicate.id()

  @cached_property
  def abort_on_fail(self) -> bool:
    return any2bool(self.resolve_prop('abort_on_fail'))

  @cached_property
  def predicate(self) -> Predicate:
    return self.inflate_child(
      Predicate,
      prop='predicate',
      resolve_kod=False
    )

  @cached_property
  def title(self):
    return super().title or self.predicate.title

  @cached_property
  def info(self):
    return super().info or self.predicate.info

  def perform(self, **kwargs) -> None:
    passed = any2bool(self.predicate.resolve())
    if not passed:
      error_type = FatalActionError if self.abort_on_fail else ActionError
      raise error_type(
        type='predicate_neg',
        name=self.predicate.id(),
        reason=self.predicate.reason,
        resource=self.predicate.culprit_res_signature()
      )


class RunPredicatesAction(MultiAction):

  @cached_property
  def sub_predicate_kods(self) -> List[KoD]:
    value = self.config.get('predicates', [])
    if not type(value) == list:
      raise RuntimeError("[kama_sdk:RunPredicatesAction] preds must be list")
    return value

  @cached_property
  def sub_actions(self) -> List[Action]:
    return [self.pred_kod2action(p) for p in self.sub_predicate_kods]

  def pred_kod2action(self, predicate_kod: KoD) -> RunPredicateAction:
    action = RunPredicateAction(dict(predicate=predicate_kod))
    action.parent = self
    return action
