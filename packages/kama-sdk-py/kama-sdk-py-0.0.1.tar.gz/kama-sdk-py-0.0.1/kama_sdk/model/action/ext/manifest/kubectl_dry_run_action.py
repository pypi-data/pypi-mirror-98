from typing import Dict, List

from werkzeug.utils import cached_property

from kama_sdk.core.ktea.ktea_client import KteaClient
from kama_sdk.model.action.base.action import Action, FatalActionError


class KubectlDryRunAction(Action):

  @cached_property
  def res_descs(self) -> List[Dict]:
    return self.get_prop('res_descs', [])

  def perform(self, **kwargs) -> None:
    success, logs = KteaClient.kubectl_dry_run(self.res_descs)
    self.add_logs(logs)
    raise_on_dry_run_err(success, logs)


def raise_on_dry_run_err(success: bool, logs):
  if not success:
    raise FatalActionError(
      type='kubectl_dry_run_failed',
      name=f"manifest was rejected",
      reason='kubectl dry_run failed for one or more resources.',
      logs=logs
    )
