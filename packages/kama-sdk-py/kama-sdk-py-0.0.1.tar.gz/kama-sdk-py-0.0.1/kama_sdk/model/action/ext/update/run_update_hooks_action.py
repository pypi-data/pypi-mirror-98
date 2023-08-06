from typing import List

from werkzeug.utils import cached_property

from kama_sdk.core.core import updates_man, utils
from kama_sdk.core.core.types import UpdateDict
from kama_sdk.model.action.base.multi_action import MultiAction
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.hook.hook import Hook


class RunUpdateHooksAction(MultiAction):

  @cached_property
  def is_injection(self) -> bool:
    return self.get_prop(IS_INJECTION_KEY)

  @cached_property
  def timing(self) -> str:
    return self.get_prop(TIMING_KEY)

  @cached_property
  def update_bundle(self) -> UpdateDict:
    update_id = self.get_prop(UPDATE_ID_KEY)
    return updates_man.fetch_update(update_id)

  @cached_property
  def hooks(self) -> List[Hook]:
    if self.is_injection:
      return updates_man.find_injection_hooks(self.timing)
    else:
      return updates_man.find_hooks(self.timing, self.update_bundle)

  @cached_property
  def sub_actions(self) -> List[Action]:
    return utils.flatten([hook.actions for hook in self.hooks])


UPDATE_ID_KEY = 'update_id'
TIMING_KEY = 'timing'
IS_INJECTION_KEY = 'is_injection'
