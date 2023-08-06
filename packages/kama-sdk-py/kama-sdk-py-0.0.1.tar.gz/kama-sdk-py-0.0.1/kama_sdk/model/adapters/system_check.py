from typing import Optional

from werkzeug.utils import cached_property

from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicatesAction


class SystemCheck(RunPredicatesAction):

  @cached_property
  def est_duration(self) -> Optional[str]:
    return self.get_prop('est_duration', [])
