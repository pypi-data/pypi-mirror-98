from typing import List

from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.types import KDLoS
from kama_sdk.model.supplier.base import supplier
from kama_sdk.model.supplier.predicate.predicate import Predicate, OPERATOR_KEY


class MultiPredicate(Predicate):

  @cached_property
  def sub_predicates(self) -> List[KDLoS]:
    return self.config.get(supplier.SRC_DATA_KEY)

  @cached_property
  def operator(self):
    return self.get_prop(OPERATOR_KEY, 'and')

  def resolve(self) -> bool:
    for sub_pred in self.sub_predicates:
      eval_or_literal = self.resolve_prop_value(sub_pred)
      resolved_to_true = utils.any2bool(eval_or_literal)

      if self.operator == 'or':
        if resolved_to_true:
          return True
      elif self.operator == 'and':
        if not resolved_to_true:
          return False
      else:
        print(f"[kama_sdk::multi_pred] illegal operator {self.operator}")
        return False
    return self.operator == 'and'
