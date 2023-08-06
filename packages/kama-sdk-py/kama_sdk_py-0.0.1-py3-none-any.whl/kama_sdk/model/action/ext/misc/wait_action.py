import time

from werkzeug.utils import cached_property

from kama_sdk.model.action.base.action import Action


class WaitAction(Action):

  @cached_property
  def title(self) -> str:
    return f"Wait {self.duration_seconds} seconds"

  @cached_property
  def info(self) -> str:
    return f"Holds the thread for the requested duration"

  @cached_property
  def duration_seconds(self) -> int:
    return int(self.get_prop('duration_seconds', 3))

  def perform(self, **kwargs) -> None:
    time.sleep(self.duration_seconds)
