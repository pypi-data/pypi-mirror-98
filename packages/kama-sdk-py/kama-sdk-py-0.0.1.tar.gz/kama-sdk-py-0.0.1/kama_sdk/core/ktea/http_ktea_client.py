from typing import Dict, List
from urllib.parse import quote_plus

import requests

from kama_sdk.core.core.types import K8sResDict
from kama_sdk.core.ktea.ktea_client import KteaClient


class HttpKteaClient(KteaClient):

  def load_default_values(self) -> Dict[str, str]:
    return self.http_get(f"/values?{self.any_cmd_args()}")

  def template_manifest(self, values: Dict) -> List[K8sResDict]:
    endpoint = f"/template?{self.template_cmd_args()}"
    return self.http_post(endpoint, values)

  def base_url(self):
    ktea = self.ktea
    version = ktea.get('version')
    version_part = f"/{version}" if version else ''
    return f"{ktea['uri']}{version_part}"

  def http_post(self, endpoint, payload):
    url = f'{self.base_url()}{endpoint}'
    response = requests.post(url, json=payload)
    return response.json().get('data')

  def http_get(self, endpoint):
    url = f'{self.base_url()}{endpoint}'
    response = requests.get(url)
    return response.json().get('data')

  def any_cmd_args(self) -> str:
    args_str = super().any_cmd_args()
    if args_str:
      return f"args={quote_plus(args_str)}"
    return ''

  def template_cmd_args(self, *args) -> str:
    std_part = self.any_cmd_args()
    if not self.release_name():
      print("[kama_sdk:ktea+client] fatal ns is blank")
    ns_part = f"release_name={self.release_name()}"
    std_part = f"&{std_part}" if std_part else ""
    return f"{ns_part}{std_part}"
