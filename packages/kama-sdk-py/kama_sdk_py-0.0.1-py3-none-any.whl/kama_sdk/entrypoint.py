from k8kat.auth.kube_broker import broker

from kama_sdk import worker, opsim, server
from kama_sdk.core.core import utils, config_man
from kama_sdk.model.base.model import models_man


def start():
  broker.connect()
  models_man.add_defaults()
  config_man.clear_trackers()

  if utils.is_server():
    server.start()
  elif utils.is_worker():
    worker.start()
  elif utils.is_opsim():
    opsim.start()
  elif utils.is_shell():
    print("Make sure you run python with -i")
  else:
    print(f"Unrecognized exec mode {utils.exec_mode()}")
