from typing import Dict

import requests

from kama_sdk.core.core.types import UpdateDict, InjectionsDesc

from kama_sdk.model.base.model import Model


app_update_id = "nectar.mock-updates.app-update"
injection_bundle_id = "nectar.mock-updates.injection"
initial_injection_bundle_id = "nectar.mock-updates.initial-injection"


class MockUpdate(Model):
  def __init__(self, config: Dict):
    super().__init__(config)
    self.version = config.get('version')
    self.note = config.get('note')
    self.ktea_type = config.get('ktea_type')
    self.ktea_uri = config.get('ktea_uri')
    if not self.note and config.get('note_url'):
      remote_note = requests.get(config.get('note_url'))
      self.note = remote_note.text

  def as_bundle(self) -> UpdateDict:
    return dict(
      id=self.id(),
      version=self.version,
      ktea_type=self.ktea_type,
      ktea_uri=self.ktea_uri,
      note=self.note,
    )

  def as_injection_bundle(self) -> InjectionsDesc:
    return dict(
      standard=self.config.get('standard'),
      inline=self.config.get('inline')
    )
