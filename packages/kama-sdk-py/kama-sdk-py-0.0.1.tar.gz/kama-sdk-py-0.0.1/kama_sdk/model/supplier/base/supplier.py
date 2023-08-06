
from typing import Any, Dict, Union, Optional

import jq
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.utils import listlike
from kama_sdk.model.base.model import Model


class Supplier(Model):

  @cached_property
  def treat_as_list(self):
    return self.get_prop(IS_MANY_KEY)

  @cached_property
  def output_format(self):
    return self.get_prop(OUTPUT_FMT_KEY)

  @cached_property
  def on_raise(self):
    return self.get_prop(ON_RAISE_KEY)

  @cached_property
  def source_data(self) -> Optional[any]:
    return self.get_prop(SRC_DATA_KEY)

  @cached_property
  def serializer_type(self) -> str:
    return self.get_prop('serializer', 'jq')

  # noinspection PyBroadException
  def resolve(self) -> Any:
    try:
      computed_value = self._compute()
      if self.serializer_type == 'legacy':
        return self.serialize_computed_value_legacy(computed_value)
      elif self.serializer_type == 'jq':
        return self.jq_serialize(computed_value)
    except:
      if ON_RAISE_KEY in self.config.keys():
        return self.on_raise
      else:
        raise

  def jq_serialize(self, computed_value) -> any:
    if self.output_format:
      try:
        expression = jq.compile(self.output_format)
        return expression.input(computed_value).first()
      except:
        return None
    else:
      return computed_value

  def serialize_computed_value_legacy(self, computed_value) -> Any:
    treat_as_list = self.treat_as_list
    if treat_as_list in [None, 'auto']:
      treat_as_list = listlike(computed_value)

    if treat_as_list and not self.output_format == '__count__':
      if listlike(computed_value):
        return [self.serialize_item(item) for item in computed_value]
      else:
        return [self.serialize_item(computed_value)]
    else:
      if not listlike(computed_value) or self.output_format == '__count__':
        return self.serialize_item(computed_value)
      else:
        item = computed_value[0] if len(computed_value) > 0 else None
        return self.serialize_item(item) if item else None

  def _compute(self) -> Any:
    return self.source_data

  def serialize_item(self, item: Any) -> Union[Dict, str]:
    fmt = self.output_format
    if not fmt or type(fmt) == str:
      return self.serialize_item_prop(item, fmt)
    elif type(fmt) == dict:
      return self.serialize_dict_item(item)
    else:
      return ''

  def serialize_dict_item(self, item):
    fmt: Dict = self.output_format
    serialized = {}
    for key, value in list(fmt.items()):
      serialized[key] = self.serialize_item_prop(item, value)
    return serialized

  # noinspection PyBroadException
  @staticmethod
  def serialize_item_prop(item: Any, prop_name: Optional[str]) -> Optional[Any]:
    if prop_name:
      if prop_name == '__count__':
        try:
          return len(item)
        except:
          return 0
      else:
        try:
          return utils.pluck_or_getattr_deep(item, prop_name)
        except:
          return None
    else:
      return item

  @classmethod
  def expr2props(cls, expr: str) -> Dict:
    parts = expr.split(" ")
    identity = parts[0]
    if identity == 'props':
      from kama_sdk.model.supplier.base.props_supplier import PropsSupplier
      identity = {'kind': PropsSupplier.__name__}
    elif identity == 'ns':
      from kama_sdk.model.supplier.base.props_supplier import PropsSupplier
      identity = {'inherit': 'nectar.suppliers.master_config.ns'}

    if len(parts) == 1:
      return identity
    elif len(parts) == 2:
      return {**identity, 'output': parts[1]}
    elif len(parts) == 3:
      return {**identity, 'output': parts[1], 'serializer': parts[3]}
    else:
      print(f"[supplier] danger un-parsable expr {expr}")
      return {}


IS_MANY_KEY = 'many'
OUTPUT_FMT_KEY = 'output'
ON_RAISE_KEY = 'on_error'
SRC_DATA_KEY = 'source'
SERIALIZER_KEY = 'serializer'
