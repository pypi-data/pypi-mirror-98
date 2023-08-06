from abc import ABC

from werkzeug.utils import cached_property

from kama_sdk.model.base.model import Model


class QuantityHumanizer(Model, ABC):

  ROUNDING_KEY = 'rounding'
  PREFIX_KEY = 'prefix'
  SUFFIX_KEY = 'suffix'

  @cached_property
  def rounding(self):
    return self.get_prop(self.ROUNDING_KEY, 0)

  @cached_property
  def prefix(self):
    return self.get_prop(self.PREFIX_KEY, '')

  @cached_property
  def suffix(self):
    return self.get_prop(self.SUFFIX_KEY, '')

  def humanize_quantity(self, raw_quantity: float) -> float:
    better_quantity = self._humanize_quantity(raw_quantity)
    if self.rounding > 0:
      return round(better_quantity, self.rounding)
    else:
      return int(better_quantity)

  def humanize_expr(self, raw_value: float) -> str:
    better_expr = self._humanize_expr(raw_value)
    return f"{self.prefix}{better_expr}{self.suffix}"

  def _humanize_expr(self, raw_value: float) -> str:
    return str(self.humanize_quantity(raw_value))

  @staticmethod
  def _humanize_quantity(value: float) -> float:
    return value
