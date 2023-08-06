from flask import Blueprint, jsonify

from kama_sdk.core.core import job_client
from kama_sdk.model.adapters.system_check import SystemCheck
from kama_sdk.serializers import system_test_serializer

controller = Blueprint('system_checks', __name__)

BASE_PATH = '/api/system_checks'

@controller.route(BASE_PATH)
def index():
  models = SystemCheck.inflate_all()
  serializer = system_test_serializer.serialize_std
  serialized = list(map(serializer, models))
  return dict(data=serialized)


@controller.route(f"{BASE_PATH}/<_id>/run", methods=['POST'])
def run(_id: str):
  if SystemCheck.inflate(_id, safely=True):
    job_id = job_client.enqueue_action(_id)
    return jsonify(status='running', job_id=job_id)
  else:
    return jsonify(error=f"no such test '{_id}'"), 400
