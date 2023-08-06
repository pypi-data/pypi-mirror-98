from kama_sdk.core.core.config_man import config_man
from kama_sdk.model.base.model import Model


class AppStatusComputer(Model):

  @classmethod
  def singleton_id(cls):
    return 'nectar.app-status-computer'

  def compute_status(self) -> str:
    eval_result = self.get_prop(PREDICATE_KEY)
    return STATUS_RUNNING if eval_result else STATUS_BROKEN

  def compute_and_commit_status(self) -> str:
    status = self.compute_status()
    config_man.write_application_status(status)
    return status


STATUS_RUNNING = 'running'
STATUS_BROKEN = 'broken'
PREDICATE_KEY = 'predicate'
