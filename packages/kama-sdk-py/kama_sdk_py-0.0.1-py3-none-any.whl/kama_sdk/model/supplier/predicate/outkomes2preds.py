from typing import List

from kama_sdk.core.core import utils, consts
from kama_sdk.core.core.types import KAO
from kama_sdk.model.supplier.predicate.predicate import Predicate


def outkomes2preds(outkomes: List[KAO]) -> List[Predicate]:
  predicates = dict(positive=[], negative=[])
  for ktl_outcome in outkomes:
    if not ktl_outcome['verb'] == 'unchanged':
      for charge in [consts.pos, consts.neg]:
        predicate = outkome2charged_pred(ktl_outcome, charge)
        predicates[charge].append(predicate)
  return utils.flatten(predicates.values())


def outkome2charged_pred(ktl_out: KAO, charge):
  from kama_sdk.model.supplier.ext.biz.resources_supplier import ResourcesSupplier
  return Predicate(dict(
    kind='Predicate',
    id=f"{ktl_out['kind']}/{ktl_out['name']}-{charge}",
    title=f"{ktl_out['kind']}/{ktl_out['name']} is {charge}",
    check_against=charge,
    optimistic=charge == consts.pos,
    operator='only',
    challenge=dict(
      kind=ResourcesSupplier.__name__,
      output='ternary_status',
      serializer='legacy',
      many=True,
      selector=dict(
        res_kind=ktl_out['kind'],
        name=ktl_out['name'],
        api_group=ktl_out['api_group']
      )
    ),
    culprit_resource_signature=dict(
      kind=ktl_out['kind'],
      name=ktl_out['name'],
      api_group=ktl_out['api_group']
    )
  ))
