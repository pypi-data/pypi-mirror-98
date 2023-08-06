from typing import Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core import config_man as cm
from kama_sdk.core.core.config_man import config_man
from kama_sdk.model.action.base.action import Action, FatalActionError


class PatchManifestVarsAction(Action):

  @cached_property
  def title(self) -> str:
    return super().title or f"Patch {self.source_key} values"

  def values(self) -> Dict:
    return self.get_prop('values') or {}

  def source_key(self) -> str:
    return self.get_prop('target_key', cm.user_vars_key)

  def perform(self) -> None:
    config_man.patch_into_deep_dict(
      self.source_key(),
      self.values()
    )


class WriteManifestVarsAction(Action):

  @cached_property
  def values(self) -> Dict:
    return self.get_prop('values') or {}

  def source_key(self) -> str:
    return self.get_prop('target_key')

  def perform(self) -> None:
    self.raise_if_illegal_source_key()
    config_man.patch_master_cmap(
      self.source_key(),
      self.values
    )

  def raise_if_illegal_source_key(self):
    reason = None
    source_key = self.source_key()
    if not source_key:
      reason = "source key must be explicit for dangerous action"
    elif source_key not in cm.manifest_var_keys:
      reason = f"source key {source_key} not in {cm.manifest_var_keys}"

    if reason:
      raise FatalActionError(
        type='write_manifest_action_illegal_key',
        reason=reason
      )
