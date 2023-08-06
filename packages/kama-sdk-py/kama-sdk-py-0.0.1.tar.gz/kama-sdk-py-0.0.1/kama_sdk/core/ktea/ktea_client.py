import os
import subprocess
import traceback
from typing import List, Optional, Dict, Tuple

import yaml
from k8kat.auth.kube_broker import broker
from k8kat.utils.main.api_defs_man import api_defs_man
from typing_extensions import TypedDict

from kama_sdk.core.core import utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import K8sResDict, KteaDict, KAO

tmp_file_mame = '/tmp/man.yaml'
ktl_apply_cmd_base = f"kubectl apply -f {tmp_file_mame}"
RESD = K8sResDict
RESDs = List[K8sResDict]

class KteaClientConstructorArgs(TypedDict):
  ktea: KteaDict


class KteaClient:

  def __init__(self, **kwargs: KteaClientConstructorArgs):
    self.ktea: KteaDict = kwargs.get('ktea') or config_man.ktea_desc()

  def load_default_values(self):
    raise NotImplemented

  def template_manifest(self, values: Dict) -> List[K8sResDict]:
    raise NotImplemented

  def template_manifest_std(self) -> List[K8sResDict]:
    value_bundle = config_man.standard_manifest_values()
    return self.template_manifest(value_bundle)

  def dry_run(self, **kwargs) -> List[Dict]:
    """
    Retrieves the manifest from Kteai, writes its contents to a temporary local
    file (filtering resources by rules), and runs kubectl apply -f on it.
    :return: any generated terminal output from kubectl apply.
    """
    res_dicts = self.template_manifest(kwargs['values'])
    return self.filter_res(res_dicts, kwargs.get('rules', []))

  def apply(self, **kwargs) -> List[KAO]:
    """
    Retrieves the manifest from Kteai, writes its contents to a temporary local
    file (filtering resources by rules), and runs kubectl apply -f on it.
    :return: any generated terminal output from kubectl apply.
    """
    return self.kubectl_apply(self.dry_run(**kwargs))

  def any_cmd_args(self) -> str:
    return self.ktea.get('args') or ''

  def template_cmd_args(self, vars_path: str) -> str:
    values_flag: str = f"-f {vars_path}"
    ns = config_man.ns()
    return f"{ns} . {values_flag} {self.any_cmd_args()}"

  @staticmethod
  def merge_ktea_vals(spec: KteaDict, values: Dict) -> Dict:
    return utils.deep_merge(
      spec.get('weak_merge', {}),
      values,
      spec.get('strong_merge', {})
    )

  @staticmethod
  def kubectl_dry_run(res_dicts: RESDs) -> Tuple[bool, List[str]]:
    with short_lived_resfile(resdicts=res_dicts):
      try:
        command_parts = ktl_apply_cmd().split(" ")
        result = subprocess.check_output(command_parts, stderr=subprocess.STDOUT)
        return True, bytes2logs(result)
      except subprocess.CalledProcessError as e:
        return False, bytes2logs(e.output)
      except:
        return False, traceback.format_exc()

  @staticmethod
  def kubectl_apply(res_dicts: RESDs) -> List[KAO]:
    """
    Kubectl applies the manifest and returns any generated terminal output.
    :return: any generated teminal output.
    """
    outcomes: List[KAO] = []
    for res_dict in res_dicts:
      with short_lived_resfile(resdict=res_dict):
        command_parts = ktl_apply_cmd().split(" ")
        # noinspection PyBroadException
        try:
          result = subprocess.check_output(command_parts, stderr=subprocess.STDOUT)
          # print(f"[kama_sdk:ktea_client] {command_parts} -----> {result}")
          outcomes.append(log2outcome(True, res_dict, result))
        except subprocess.CalledProcessError as e:
          print(traceback.format_exc())
          print(f"[kama_sdk:ktea_client] CalledProcessError {command_parts} ^^")
          outcomes.append(log2outcome(False, res_dict, e.output))
        except:
          print(traceback.format_exc())
          print(f"[kama_sdk:ktea_client] Unknown error {command_parts} ^^")
          outcomes.append(log2outcome(False, res_dict, traceback.format_exc()))
    return [o for o in outcomes if o]

  @staticmethod
  def filter_res(res_list: RESDs, selectors) -> RESDs:
    """
    Filters the list of parsed kubernetes resources from the tami-generated
    application manifest according to the passed rule-set.
    :param res_list: k8s resource list to be filtered.
    :param selectors: rules to be used for filtering.
    :return: filtered resource list.
    """
    def decide_res(res):
      for selector in selectors:
        if selector.selects_res(res):
          return True
      return False
    if selectors:
      return list(filter(decide_res, res_list))
    else:
      return res_list

  @staticmethod
  def release_name():
    return config_man.ns()


def bytes2logs(output) -> List[str]:
  raw_log = output.decode('utf-8') if output else ''
  parts = raw_log.split("\n")
  # print(f"parts {parts}")
  # raw_log = parts[0] if len(parts) == 2 else None
  # print(f"rawlog {raw_log}")
  return parts


def log2outcome(succs: bool, resdict: RESD, output) -> Optional[KAO]:
  raw_log = output.decode('utf-8') if output else ''
  parts = raw_log.split("\n")
  raw_log = parts[0] if len(parts) == 2 else None

  if raw_log:
    if succs:
      return utils.log2kao(raw_log)
    else:
      kind = resdict.get('kind')
      kind = api_defs_man.kind2plurname(kind) or kind
      api_group = api_defs_man.find_api_group(kind)
      return KAO(
        api_group=api_group,
        kind=kind,
        name=resdict.get('metadata', {}).get('name'),
        verb=None,
        error=raw_log
      )
  else:
    print(f"[kama_sdk::ktea_client] panic log fmt unknown: {raw_log}")
    return None


class short_lived_resfile:
  def __init__(self, **kwargs):
    resdict: K8sResDict = kwargs.get('resdict')
    resdicts: List[K8sResDict] = kwargs.get('resdicts')
    self.res_dict = resdict
    self.res_dicts = resdicts

  def __enter__(self):
    with open(tmp_file_mame, 'w') as file:
      if self.res_dict is not None:
        file.write(yaml.dump(self.res_dict))
      elif self.res_dicts is not None:
        file.write(yaml.dump_all(self.res_dicts))

  def __exit__(self, exc_type, exc_val, exc_tb):
    if os.path.isfile(tmp_file_mame):
      if utils.is_prod():
        os.remove(tmp_file_mame)


def ktl_apply_cmd() -> str:
  final_cmd = ktl_apply_cmd_base
  if utils.is_out_of_cluster():
    if broker.connect_config.get('context'):
      context_part = f"--context={broker.connect_config['context']}"
      final_cmd = f"{final_cmd} {context_part}"
  return final_cmd
