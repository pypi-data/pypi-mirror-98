from typing import List, TypeVar, Dict

from werkzeug.utils import cached_property

from kama_sdk.model.action.base.action import Action
from kama_sdk.model.base.model import Model

T = TypeVar('T', bound='Hook')

class Hook(Model):

  ACTIONS_KEY = 'misc'
  TRIGGER_SELECTOR_KEY = 'trigger_selector'

  @cached_property
  def actions(self) -> List[Action]:
    return self.inflate_children(Action, prop=self.ACTIONS_KEY)

  @cached_property
  def trigger_selector(self) -> Dict:
    return self.get_prop(self.TRIGGER_SELECTOR_KEY) or {}

  def subscribes_to(self, **labels) -> bool:
    selector_items = self.trigger_selector.items()
    if len(selector_items) > 0:
      return selector_items <= labels.items()
    else:
      return False

  @classmethod
  def by_trigger(cls, **labels) -> List[T]:
    all_hooks = cls.inflate_all()
    filterer = lambda hook: hook.subscribes_to(**labels)
    return list(filter(filterer, all_hooks))
