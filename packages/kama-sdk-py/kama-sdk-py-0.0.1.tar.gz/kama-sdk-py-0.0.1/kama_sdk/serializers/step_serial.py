from typing import Dict

from kama_sdk.core.core.config_man import config_man
from kama_sdk.model.operation.field import Field
from kama_sdk.model.input import input_serializer
from kama_sdk.model.operation.operation_state import OperationState
from kama_sdk.model.operation.step import Step


def ser_embedded_field(field: Field, value, state: OperationState) -> Dict:
  current_or_default = field.variable.current_or_default_value()
  decorated_value = None
  decorator = field.variable.value_decorator

  if decorator and decorator.compute_visibility():
    value = current_or_default if not value else value
    decorated_value = decorator.decorate(value, state)

  return dict(
    id=field.id(),
    title=field.title,
    info=field.info,
    is_inline=field.is_inline_chart_var(),
    default=current_or_default,
    decorated_value=decorated_value,
    **input_serializer.in_variable(field.variable.input_model),
  )


def ser_refreshed(step: Step, values: Dict, state: OperationState) -> Dict:
  """
  Standard serializer for a step.
  :param step: Step class instance.
  :param values: current user input
  :param state: current operation state
  :return: serialized Step in dict form.
  """
  config_man.user_vars()
  visible_fields = step.visible_fields(values, state)
  serialize_field = lambda field: ser_embedded_field(
    field=field,
    value=(values or {}).get(field.id()),
    state=state
  )
  return dict(
    id=step.id(),
    title=step.title,
    info=step.info,
    flags=[],
    fields=list(map(serialize_field, visible_fields))
  )
