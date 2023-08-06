from typing import Dict

from kama_sdk.model.base.model import Model


class InputOption(Model):
  def serialize(self) -> Dict:
    return {
      'id': self.id(),
      'title': self.title
    }
