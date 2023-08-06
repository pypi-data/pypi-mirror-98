from typing import Dict

from kama_sdk.model.adapters.system_check import SystemCheck
from kama_sdk.model.supplier.predicate.predicate import Predicate


def serialize_embedded_pred(predicate: Predicate) -> Dict:
  return dict(
    title=predicate.title,
    info=predicate.info
  )


def serialize_std(check: SystemCheck) -> Dict:
  return dict(
    id=check.id(),
    title=check.title,
    info=check.info,
    length=len(check.sub_predicate_kods),
    est_duration=check.est_duration,
    predicates=list(map(serialize_embedded_pred, check.sub_predicate_kods))
  )
