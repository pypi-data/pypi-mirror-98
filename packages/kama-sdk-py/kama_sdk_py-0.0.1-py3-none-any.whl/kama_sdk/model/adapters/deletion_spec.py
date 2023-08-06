from kama_sdk.model.base.model import Model


class DeletionSpec(Model):
  def __init__(self, config):
    super().__init__(config)
    self.groups = config.get('victim_groups')
