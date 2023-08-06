from typing import Any, Optional

from werkzeug.utils import cached_property

from kama_sdk.model.supplier.base.supplier import Supplier


class ContextSupplier(Supplier):

  def orig_output_format(self) -> Optional[str]:
    return super().output_format

  @cached_property
  def output_format(self):
    orig = self.orig_output_format()
    if orig and type(orig) == str:
      return orig.split('.')[1:]
    else:
      return orig

  def source_data(self) -> Optional[Any]:
    master_key = self.orig_output_format().split('.')[0]
    return self.resolve_context_value(master_key)
