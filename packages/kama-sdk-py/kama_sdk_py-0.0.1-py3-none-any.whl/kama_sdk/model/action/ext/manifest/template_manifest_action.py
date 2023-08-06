from typing import List, Optional, Any, Dict

import yaml
from typing_extensions import TypedDict
from werkzeug.utils import cached_property

from kama_sdk.core.core.types import K8sResDict, KteaDict
from kama_sdk.core.ktea.ktea_client import KteaClient
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.action.base.action import Action, FatalActionError
from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector


class OutputFormat(TypedDict):
  res_descs: List[K8sResDict]


class TemplateManifestAction(Action):

  @cached_property
  def ktea(self) -> KteaDict:
    return self.resolve_prop('ktea')

  @cached_property
  def values(self) -> Dict:
    return self.resolve_prop('values')

  @cached_property
  def selectors(self) -> List[ResourceSelector]:
    return self.resolve_prop('selectors')

  def perform(self, **kwargs) -> OutputFormat:
    client_inst = ktea_client(ktea=self.ktea)
    values = KteaClient.merge_ktea_vals(self.ktea, self.values)
    res_descs = client_inst.template_manifest(values)
    self.check_failures(self.ktea, res_descs)
    res_descs = client_inst.filter_res(res_descs, self.selectors)

    self.add_logs(list(map(yaml.dump, res_descs)))
    return dict(res_descs=res_descs)

  def check_failures(self, ktea, res_descs: Optional[Any]):
    if res_descs is None:
      raise FatalActionError(
        type=self.default_error_type(),
        reason='ktea client returned None',
        extras=dict(ktea=ktea)
      )

  def default_error_type(self):
    return 'template_manifest_failed'
