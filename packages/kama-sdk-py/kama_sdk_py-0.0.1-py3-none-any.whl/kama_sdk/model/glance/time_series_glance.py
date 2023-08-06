from datetime import datetime
from typing import List, Optional, Dict

import humanize
from werkzeug.utils import cached_property

from kama_sdk.core.core.types import TimeSeriesDataPoint
from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor
from kama_sdk.model.humanizer.quantity_humanizer import QuantityHumanizer


class TimeSeriesGlance(GlanceDescriptor):

  @cached_property
  def view_type(self) -> str:
    return 'line_chart'

  @cached_property
  def info(self):
    if len(self.time_series) > 0:
      ts0 = self.time_series[0]['timestamp']
      delta_str = humanize.naturaltime(datetime.fromisoformat(ts0))
      return f"{delta_str} - now"
    else:
      return "Not enough data"

  @cached_property
  def time_series(self) -> List[TimeSeriesDataPoint]:
    return self.get_prop(DATA_KEY, [])

  @cached_property
  def reducer_type(self) -> str:
    return self.get_prop(REDUCER_FUNC_KEY, 'last')

  def change_direction(self) -> str:
    # count = len(self.time_series)
    # if count >= 2:
    #   last = self.time_series
    return 'up'

  @cached_property
  def good_direction(self) -> bool:
    return self.get_prop(GOOD_DIRECTION_KEY, 'up')

  @cached_property
  def humanizer(self) -> QuantityHumanizer:
    return self.inflate_child(
      QuantityHumanizer,
      prop=HUMANIZER_KEY,
      safely=True
    ) or QuantityHumanizer({})

  # noinspection PyBroadException
  def summary_quant(self) -> Optional[float]:
    try:
      if self.reducer_type == 'last':
        return _last_data_point(self.time_series)
      elif self.reducer_type == 'sum':
        return _series_sum(self.time_series)
    except:
      return None

  def gen_legend(self):
    return {
      **super().gen_legend(),
      'direction': self.change_direction(),
      'good_direction': self.good_direction
    }

  def content_spec(self):
    series = [humanize_datapoint(d, self.humanizer) for d in self.time_series]
    return {
      'timeseries': series,
      'value': self.humanizer.humanize_expr(self.summary_quant()),
      'xKey': 'timestamp',
      'yKey': 'value'
    }


def humanize_datapoint(datapoint, humanizer: QuantityHumanizer):
  return {
    **datapoint,
    'value': humanizer.humanize_quantity(datapoint['value'])
  }


def _last_data_point(series: List[Dict]) -> Optional[float]:
  if len(series) > 0:
    return series[len(series) - 1]['value']
  else:
    return None


def _series_sum(series: List[TimeSeriesDataPoint]) -> float:
  return sum([float(d['value'] or 0) for d in series])


def _series_avg(series: List[TimeSeriesDataPoint]) -> float:
  try:
    return _series_sum(series) / len(series)
  except ValueError:
    return 0.0


DATA_KEY = 'time_series_data'
REDUCER_FUNC_KEY = 'reducer'
HUMANIZER_KEY = 'humanizer'
GOOD_DIRECTION_KEY = 'good_direction'
