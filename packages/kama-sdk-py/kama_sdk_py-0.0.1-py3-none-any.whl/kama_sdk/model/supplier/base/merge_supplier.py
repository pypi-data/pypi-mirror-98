from typing import Dict, List, Any

from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.model.supplier.base.supplier import Supplier


class MergeSupplier(Supplier):

  @cached_property
  def source_data(self) -> List[Dict]:
    dicts = super(MergeSupplier, self).source_data
    return [d or {} for d in dicts]

  def _compute(self) -> Any:
    return utils.deep_merge(*self.source_data)
