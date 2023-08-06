from typing import Dict, List, Any, Optional
from werkzeug.utils import cached_property
from kama_sdk.model.base.model import Model
from kama_sdk.model.input.select_option import InputOption


class GenericInput(Model):

  @cached_property
  def option_models(self) -> List[InputOption]:
    return self.inflate_children(InputOption,  prop=KEY_OPTIONS)

  def compute_inferred_default(self) -> Optional[Any]:
    _serialized_options = self.serialize_options()
    if len(_serialized_options) > 0:
      return _serialized_options[0].get('id')
    return None

  def serialize_options(self) -> List:
    return list(map(InputOption.serialize, self.option_models))

  def extras(self) -> Dict[str, any]:
    return {}

  @staticmethod
  def sanitize_for_validation(value: Any) -> Any:
    return value


KEY_OPTIONS = 'options'
