from k8kat.auth.kube_broker import broker

from kama_sdk.model.base.model import models_man

broker.connect(dict(
  auth_type='kube-config',
  context='wear'
))

models_man.add_defaults()

print("[kama_sdk::shell] loaded packages for shell mode")