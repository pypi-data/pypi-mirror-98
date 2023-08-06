from typing import Any, Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core import subs
from kama_sdk.model.base.model import Model
from kama_sdk.model.operation.operation_state import OperationState


class VariableValueDecorator(Model):

  @cached_property
  def output_template(self) -> str:
    return self.get_prop(KEY_TEMPLATE, '')

  def compute_visibility(self) -> bool:
    return self.resolve_prop(SHOW_COND_KEY, backup=True)

  def decorate(self, value: Any, operation_state: OperationState) -> Any:
    subs2 = self.compute(value, operation_state) or {}
    return subs.interp_str(self.output_template, subs2)

  def compute(self, value: Any, operation_state: OperationState) -> Dict:
    return {}


KEY_TEMPLATE = 'template'
SHOW_COND_KEY = 'visible'
