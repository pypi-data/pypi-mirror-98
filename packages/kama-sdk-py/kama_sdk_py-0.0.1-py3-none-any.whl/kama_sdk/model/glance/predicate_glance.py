from werkzeug.utils import cached_property

from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor
from kama_sdk.model.supplier.predicate.predicate import Predicate


class PredicateGlance(GlanceDescriptor):
  PREDICATE_KEY = 'predicate'
  PASS_TEXT_KEY = 'pass_text'
  FAIL_TEXT_KEY = 'fail_text'
  PASS_ICON_KEY = 'pass_icon'
  FAIL_ICON_KEY = 'fail_icon'

  @cached_property
  def view_type(self) -> str:
    return "resource"

  @cached_property
  def predicate(self):
    return self.inflate_child(
      Predicate,
      prop=self.PREDICATE_KEY
    )

  @cached_property
  def pass_text(self):
    return self.get_prop(self.PASS_TEXT_KEY, 'Passing')

  @cached_property
  def fail_text(self):
    return self.get_prop(self.FAIL_TEXT_KEY, 'Failing')

  @cached_property
  def pass_icon(self) -> str:
    return self.get_prop(self.PASS_ICON_KEY, 'policy')

  @cached_property
  def fail_icon(self) -> str:
    return self.get_prop(self.FAIL_ICON_KEY, 'report_gmailerrorred')

  def eval_result(self) -> bool:
    return any2bool(self.predicate.resolve())

  def content_spec(self):
    success = self.eval_result()
    return {
      'graphic_type': 'icon',
      'graphic': self.pass_icon if success else self.fail_icon,
      'line_one': 'Workloads',
      'line_two': 'Statuses',
      'line_three': '12 Checked',
      'emotion': 'primaryColor' if success else 'lightGrey'
    }
