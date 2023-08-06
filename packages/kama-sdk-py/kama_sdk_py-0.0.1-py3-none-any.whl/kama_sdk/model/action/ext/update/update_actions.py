from typing import Optional, Dict

from werkzeug.utils import cached_property

from kama_sdk.core.core import updates_man, hub_api_client
from kama_sdk.core.core.types import UpdateDict, InjectionsDesc, KteaDict
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.action.base.action import Action, FatalActionError


class LoadVarDefaultsFromKtea(Action):

  def ktea(self) -> KteaDict:
    return self.resolve_prop('ktea')

  def perform(self, **kwargs) -> Optional[Dict]:
    client = ktea_client(ktea=self.ktea())
    variable_defaults = client.load_default_values()
    raise_if_none_defaults(variable_defaults)
    return dict(variable_defaults=variable_defaults)


def raise_if_none_defaults(defaults: Optional[Dict]):
  if not defaults:
    raise FatalActionError(
      type='load_defaults_err',
      reason='ktea returned nil for defaults'
    )


class FetchUpdateAction(Action):

  def update_id(self) -> str:
    return self.resolve_prop('update_id')

  def perform(self, **kwargs) -> Optional[UpdateDict]:
    update = updates_man.fetch_update(self.update_id())
    self.raise_if_none(update)
    return dict(update=update)

  def raise_if_none(self, update: Optional[UpdateDict]) -> None:
    if not update:
      host = hub_api_client.backend_host()
      raise FatalActionError(
        name='fetch_update',
        reason=f"fetch failed update id={self.update_id()} host {host}"
      )


class FetchInjectionBundle(Action):

  def perform(self, **kwargs) -> Optional[InjectionsDesc]:
    injection = updates_man.latest_injection_bundle()
    self.raise_on_bundle_na(injection)
    return dict(injection=injection)

  @staticmethod
  def raise_on_bundle_na(injection_bundle: Optional[InjectionsDesc]):
    if not injection_bundle:
      host = hub_api_client.backend_host()
      raise FatalActionError(
        name='fetch_injections',
        reason=f"Negative response from Nectar API ({host})"
      )


class CommitKteaFromUpdateAction(Action):

  @cached_property
  def update(self) -> UpdateDict:
    return self.get_prop('update')

  def perform(self, **kwargs) -> None:
    updates_man.commit_new_ktea(self.update)
