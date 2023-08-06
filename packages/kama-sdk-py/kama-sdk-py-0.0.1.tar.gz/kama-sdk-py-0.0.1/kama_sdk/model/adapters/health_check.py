from typing import Dict, List

from kama_sdk.model.base.model import Model
from kama_sdk.model.supplier.predicate.predicate import Predicate


class HealthChecksAdapter(Model):
  def __init__(self, config: Dict):
    super().__init__(config)
    self.use_liveness = config.get('use_liveness', True)

  def predicates(self) -> List[Predicate]:
    expl_children = self.inflate_children('predicates', Predicate)
    return [
      *self.gen_liveness_predicates(),
      expl_children
    ]

  def gen_liveness_predicates(self) -> List[Predicate]:
    pass
