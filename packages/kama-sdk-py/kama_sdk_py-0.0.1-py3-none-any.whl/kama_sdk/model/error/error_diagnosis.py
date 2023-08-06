from typing import List, Optional

from werkzeug.utils import cached_property

from kama_sdk.model.base.model import Model
from kama_sdk.model.error.diagnosis_actionable import DiagnosisActionable
from kama_sdk.model.supplier.predicate.predicate import Predicate


class ErrorDiagnosis(Model):

  @cached_property
  def predicate(self) -> Optional[Predicate]:
    return self.inflate_child(
      Predicate,
      prop=PREDICATE_KEY
    )

  @cached_property
  def actionables(self) -> List[DiagnosisActionable]:
    return self.inflate_children(DiagnosisActionable, prop=ACTIONABLES_KEY)

  def compute_is_suitable(self) -> bool:
    return self.resolve_prop(PREDICATE_KEY)


PREDICATE_KEY = 'predicate'
ACTIONABLES_KEY = 'actionables'
