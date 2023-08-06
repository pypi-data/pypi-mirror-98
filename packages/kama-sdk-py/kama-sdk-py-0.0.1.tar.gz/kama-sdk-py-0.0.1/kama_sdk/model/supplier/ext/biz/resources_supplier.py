from typing import List

from k8kat.res.base.kat_res import KatRes
from werkzeug.utils import cached_property

from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector
from kama_sdk.model.supplier.base import supplier as sup
from kama_sdk.model.supplier.base.supplier import Supplier


class ResourcesSupplier(Supplier):

  @cached_property
  def serializer_type(self) -> str:
    return self.get_prop(sup.SERIALIZER_KEY, 'legacy')

  @cached_property
  def output_format(self):
    super_value = super().output_format
    if super_value == 'options_format':
      return dict(id='name', title='name')
    return super_value

  @cached_property
  def resource_selector(self) -> ResourceSelector:
    return self.inflate_child(
      ResourceSelector,
      prop=RESOURCE_SELECTOR_KEY
    )

  def _compute(self) -> List[KatRes]:
    result = self.resource_selector.query_cluster()
    return result

  def serialize_prop(self):
    pass


RESOURCE_SELECTOR_KEY = 'selector'
