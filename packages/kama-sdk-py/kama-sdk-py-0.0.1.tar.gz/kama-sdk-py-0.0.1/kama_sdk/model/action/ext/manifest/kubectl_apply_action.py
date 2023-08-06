from typing import List, Dict

from typing_extensions import TypedDict
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.types import KAO
from kama_sdk.core.ktea.ktea_client import KteaClient
from kama_sdk.model.action.base.action import Action, FatalActionError

class OutputFormat(TypedDict):
  outkomes: List[KAO]


class KubectlApplyAction(Action):

  @cached_property
  def res_descs(self) -> List[Dict]:
    return self.get_prop('res_descs')

  def perform(self, **kwargs) -> OutputFormat:
    outkomes = KteaClient.kubectl_apply(self.res_descs)
    self.add_logs(list(map(utils.kao2log, outkomes)))
    check_kao_failures(outkomes)
    return dict(outkomes=outkomes)


def is_outkome_error(outkome: KAO) -> bool:
  return outkome.get('error') is not None


def check_kao_failures(outcomes: List[KAO]):
  kao_culprit = next(filter(is_outkome_error, outcomes), None)
  if kao_culprit is not None:
    res_name = kao_culprit.get('name')
    res_kind = kao_culprit.get('kind')
    raise FatalActionError(
      type='kubectl_apply_failed',
      name=f"{res_kind}/{res_name} rejected",
      reason='kubectl apply failed for one or more resources.',
      resource=dict(name=res_name, kind=res_kind),
      logs=[kao_culprit.get('error')]
    )
