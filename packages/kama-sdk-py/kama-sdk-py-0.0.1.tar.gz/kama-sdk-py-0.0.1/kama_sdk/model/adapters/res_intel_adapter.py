import traceback
from typing import List, TypeVar

from k8kat.res.base.kat_res import KatRes
from k8kat.utils.main.types import IntelDict
from werkzeug.utils import cached_property

from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector
from kama_sdk.model.base.model import Model

T = TypeVar('T', bound='ResIntelProvider')

class ResIntelProvider(Model):

  RESOURCE_SELECTOR_KEY = 'resource_selector'

  @cached_property
  def selector(self) -> ResourceSelector:
    return self.inflate_child(
      ResourceSelector,
      prop=self.RESOURCE_SELECTOR_KEY
    )

  def covers_res(self, res: KatRes) -> bool:
    if self.selector and res and res.raw:
      return self.selector.selects_res(res.raw.to_dict())
    else:
      print("[kama_sdk:res_intel_adapter] no selector or res")

  # noinspection PyMethodMayBeStatic,PyBroadException
  def generate_intel(self, res: KatRes) -> List[IntelDict]:
    try:
      if res.ternary_status() == 'negative':
        return res.intel()
      else:
        return []
    except:
      print(traceback.format_exc())
      print("[kama_sdk:res_intel_adapter] exception generating intel ^^")
      return []

  @classmethod
  def weight(cls):
    return 0

  @classmethod
  def covering_res(cls: T, res: KatRes) -> List[T]:
    decide = lambda adapter: adapter.covers_res(res)
    return list(filter(decide, cls.inflate_all()))
