from typing import Any, Optional

from werkzeug.utils import cached_property

from kama_sdk.model.supplier.base.supplier import Supplier


class PropsSupplier(Supplier):

  def orig_output_format(self) -> Optional[str]:
    return self.config.get('output')

  @cached_property
  def default_lookback(self):
    return self.config.get('lookback', True)

  @cached_property
  def source_data(self) -> Optional[Any]:
    master_key = self.orig_output_format().split('->')[0]
    return self.resolve_prop(master_key)

  @cached_property
  def output_format(self):
    orig = self.orig_output_format()
    if orig and type(orig) == str:
      parts = orig.split('->')
      return parts[1] if len(parts) > 1 else None
    else:
      return orig
