from werkzeug.utils import cached_property

from kama_sdk.core.core.types import EndpointDict
from kama_sdk.model.base.model import TITLE_KEY
from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor


class EndpointGlance(GlanceDescriptor):
  ENDPOINT_DATA_KEY = 'endpoint'
  LINE_ONE_KEY = 'line_one'
  LINE_TWO_KEY = 'line_two'
  LINE_THREE_KEY = 'line_three'
  SITE_LOGO_KEY = 'site_logo'
  BACKUP_ICON_KEY = 'backup_icon'
  ICON_CONNECTED_KEY = 'icon_not_connected'
  ICON_NOT_CONNECTED_KEY = 'icon_not_connected'

  @cached_property
  def title(self):
    return self.get_prop(TITLE_KEY, 'App Endpoint')

  @property
  def icon_not_connected(self) -> str:
    backup = 'error_outline'
    return self.get_prop(self.ICON_NOT_CONNECTED_KEY, backup)

  @property
  def icon_connected(self) -> str:
    backup = 'open_in_new'
    return self.get_prop(self.ICON_CONNECTED_KEY, backup)

  @cached_property
  def image(self):
    return

  @cached_property
  def view_type(self):
    return 'resource'

  @cached_property
  def line_one(self):
    explicit = self.get_prop(self.LINE_ONE_KEY)
    if not explicit:
      result = self.endpoint_data
      return result['svc_type'] if result else 'Type Unknown'
    else:
      return explicit

  @cached_property
  def line_two(self):
    explicit = self.get_prop(self.LINE_TWO_KEY)
    if not explicit:
      result = self.endpoint_data
      return result['url'] if result else 'No URL'
    else:
      return explicit

  @cached_property
  def line_three(self):
    explicit = self.get_prop(self.LINE_THREE_KEY)
    if not explicit:
      result = self.endpoint_data
      return 'Public'
    else:
      return explicit

  @cached_property
  def url_intent(self) -> str:
    return self.endpoint_data.get('url')

  @cached_property
  def endpoint_data(self) -> EndpointDict:
    return self.get_prop(self.ENDPOINT_DATA_KEY)

  @cached_property
  def info(self) -> str:
    return 'Site Online' if self.is_working() else 'Site Offline'

  @cached_property
  def legend_icon(self) -> str:
    return self.icon_connected if self.is_working() \
      else self.icon_not_connected

  @cached_property
  def legend_emotion(self) -> str:
    return 'primaryColor' if self.is_working() else 'black'

  def is_working(self) -> bool:
    if self.endpoint_data:
      return self.endpoint_data.get('url') is not None
    else:
      return False

  @cached_property
  def site_logo(self):
    return self.get_prop(self.SITE_LOGO_KEY)

  @cached_property
  def backup_icon(self):
    return self.get_prop(self.BACKUP_ICON_KEY, 'language')

  def content_spec(self):
    return {
      'line_one': self.line_one,
      'line_two': self.line_two,
      'line_three': self.line_three,
      'graphic_type': 'image' if self.site_logo else 'icon',
      'graphic': self.site_logo or self.backup_icon
    }
