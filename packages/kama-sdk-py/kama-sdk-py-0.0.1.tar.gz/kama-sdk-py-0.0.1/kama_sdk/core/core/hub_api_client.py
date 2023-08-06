from typing import Optional, Dict

import requests

from kama_sdk.core.core import utils
from kama_sdk.core.core.config_man import config_man

api_path = '/cli'


def backend_host() -> Optional[str]:
  if config_man.is_training_mode():
    print("[kama_sdk:hub_client] illegal call while training mode")
    return None
  if utils.is_dev():
    if utils.is_in_cluster():
      return "http://necthub.com.ngrok.io"
    else:
      return "http://localhost:3000"
  else:
    return 'https://api.codenectar.com'


def post(endpoint, payload) -> requests.Response:
  url = f'{backend_host()}{api_path}{endpoint}'
  print(f"[kama_sdk:hub_client] post {url}")
  return requests.post(
    url,
    json=payload,
    headers=gen_headers()
  )


def patch(endpoint, payload) -> requests.Response:
  url = f'{backend_host()}{api_path}{endpoint}'
  print(f"[kama_sdk:hub_client] patch {url}")
  return requests.patch(
    url,
    json=payload,
    headers=gen_headers()
  )


def get(endpoint) -> requests.Response:
  url = f'{backend_host()}{api_path}{endpoint}'
  print(f"[kama_sdk:hub_client] get {url}")
  return requests.get(
    url,
    headers=gen_headers()
  )

def gen_headers() -> Dict:
  access_token = config_man.install_token()
  print(f"USING ACCESS TOK {access_token}")
  return {
    'Token': access_token
  }
