from typing import List, Optional

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import KteaDict
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector
from kama_sdk.model.base.model import Model


class InjectionOrchestrator(Model):

  @classmethod
  def singleton_id(cls):
    return 'nectar.injection-orchestrators.main'

  @cached_property
  def ktea(self) -> Optional[KteaDict]:
    return self.get_prop(KTEA_KEY, DEFAULT_KTEA)

  @cached_property
  def apply_selectors(self) -> List[ResourceSelector]:
    return self.inflate_children(
      ResourceSelector,
      prop=RES_SELECTORS_KEY
    )


DEFAULT_KTEA = {
  'type': 'server',
  'uri': 'https://api.codenectar.com/services/ktea/nectar/vals2sec/1.0.0'
}


RES_SELECTORS_KEY = 'apply_selectors'
KTEA_KEY = 'ktea'
