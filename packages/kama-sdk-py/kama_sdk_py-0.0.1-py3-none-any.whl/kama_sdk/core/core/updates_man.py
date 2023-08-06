from datetime import datetime
from typing import Dict, List, Optional

from kama_sdk.core.core import hub_api_client, utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import UpdateDict, InjectionsDesc, K8sResDict
from kama_sdk.core.core.utils import deep_merge
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.adapters import mock_update
from kama_sdk.model.adapters.injection_orchestrator import InjectionOrchestrator
from kama_sdk.model.adapters.mock_update \
  import MockUpdate
from kama_sdk.model.hook.hook import Hook


def is_using_latest_injection() -> bool:
  bundle = latest_injection_bundle()
  return bundle is None


def fetch_next_update() -> Optional[UpdateDict]:
  config_man.write_last_update_checked(str(datetime.now()))
  return None


def latest_injection_bundle() -> Optional[InjectionsDesc]:
  if config_man.is_real_deployment():
    resp = hub_api_client.get('/injectors/compile')
    if resp.ok:
      return resp.json()['data']
    else:
      print(f"[kama_sdk::updates_man] err requesting injection {resp.status_code}")
      return None
  else:
    model = MockUpdate.inflate(mock_update.injection_bundle_id)
    return model.as_injection_bundle()


def fetch_update(update_id: str) -> Optional[UpdateDict]:
  if config_man.is_real_deployment() and not utils.is_test():
    resp = hub_api_client.get(f'/app_updates/{update_id}')
    if resp.ok:
      return resp.json()['bundle']
    else:
      print(f"[kama_sdk::updates_man] err requesting update {resp.status_code}")
  else:
    model = MockUpdate.inflate(update_id)
    return model.as_bundle()


def next_available() -> Optional[UpdateDict]:
  if config_man.is_real_deployment():
    resp = hub_api_client.get(f'/app_updates/available')
    data = resp.json() if resp.status_code < 205 else None
    return data['bundle'] if data else None
  else:
    model = MockUpdate.inflate(mock_update.app_update_id)
    return model.as_bundle()


def _gen_injection_telem(keys: List[str]):
  all_vars = config_man.user_vars()
  return {k: all_vars[k] for k in keys}


def find_hooks(timing: str, update: UpdateDict) -> List[Hook]:
  return Hook.by_trigger(
    event='software-update',
    timing=timing,
    **update
  )


def find_injection_hooks(timing: str) -> List[Hook]:
  return Hook.by_trigger(
    event='injection',
    timing=timing
  )


def preview_injection(injection: InjectionsDesc) -> Dict:
  old_defaults = config_man.default_vars()
  old_manifest = ktea_client().template_manifest_std()

  orchestrator = InjectionOrchestrator.inflate_singleton()
  new_defaults = deep_merge(old_defaults, injection['standard'])

  new_resources = []
  if len(injection['inline']) > 0:
    new_resources = ktea_client().dry_run(
      values=injection['inline'],
      rules=orchestrator.apply_selectors
    )

  new_manifest = [r for r in old_manifest]

  def find_twin(res: K8sResDict) -> Optional[int]:
    for (i, _res) in enumerate(new_manifest):
      if utils.same_res(res, _res):
        return i
    return None

  for new_res in new_resources:
    old_version_ind = find_twin(new_res)
    if old_version_ind:
      old_version = new_manifest[old_version_ind]
      new_manifest[old_version_ind] = deep_merge(old_version, new_res)
    else:
      new_manifest.append(new_res)

  return dict(
    defaults=dict(
      old=old_defaults,
      new=new_defaults
    ),
    manifest=dict(
      old=old_manifest,
      new=new_manifest
    )
  )


def preview(update_dict: UpdateDict) -> Dict:
  old_defaults = config_man.default_vars()
  old_manifest = ktea_client().template_manifest_std()

  new_ktea = updated_release_ktea(update_dict)
  new_ktea_client = ktea_client(ktea=new_ktea)

  new_defaults = new_ktea_client.load_default_values()
  new_manifest_vars = deep_merge(new_defaults, config_man.user_vars())
  new_manifest = new_ktea_client.template_manifest(new_manifest_vars)

  return dict(
    defaults=dict(
      old=old_defaults,
      new=new_defaults
    ),
    manifest=dict(
      old=old_manifest,
      new=new_manifest
    )
  )


def commit_new_ktea(update_dict: UpdateDict):
  new_ktea = updated_release_ktea(update_dict)
  config_man.patch_ktea(new_ktea)


def commit_new_defaults_from_update(update_dict: UpdateDict):
  new_ktea = updated_release_ktea(update_dict)
  new_defaults = ktea_client(ktea=new_ktea).load_default_values()
  config_man.patch_def_vars(new_defaults)


def updated_release_ktea(update: UpdateDict) -> Dict:
  new_ktea = dict(version=update['version'])
  if update.get('ktea_type'):
    new_ktea['type'] = update.get('ktea_type')
  if update.get('ktea_uri'):
    new_ktea['uri'] = update.get('ktea_uri')
  return {**config_man.ktea_desc(), **new_ktea}
