from typing import Dict

from kama_sdk.core.core import job_client
from kama_sdk.core.core.types import KoD
from kama_sdk.model.base.model import Model


class DiagnosisActionable(Model):
  def __init__(self, config: Dict):
    super().__init__(config)
    self.action_kod: KoD = config.get('action')
    self.operation_id: str = config.get('operation_id')

  def run_action(self):
    return job_client.enqueue_action(self.action_kod)
