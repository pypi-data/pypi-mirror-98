from flask import Blueprint, jsonify

from kama_sdk.core.core import updates_man, job_client
from kama_sdk.model.action.ext.update.run_update_hooks_action import RunUpdateHooksAction

controller = Blueprint('injections_controller', __name__)

BASE_PATH = '/api/injections'

@controller.route(f'{BASE_PATH}/check_newer')
def check_newer():
  new_available = not updates_man.is_using_latest_injection()
  return jsonify(data=new_available)


@controller.route(f'{BASE_PATH}/latest/preview')
def preview():
  bundle = updates_man.latest_injection_bundle()
  preview_data = updates_man.preview_injection(bundle)
  return jsonify(data=preview_data)


@controller.route(f'{BASE_PATH}/latest/hooks/<timing>/run', methods=['POST'])
def run_injection_hooks(timing: str):
  job_id = job_client.enqueue_action({
    'kind': RunUpdateHooksAction.kind(),
    'is_injection': True,
    'timing': timing
  })
  return jsonify(data=(dict(job_id=job_id)))


@controller.route(f'{BASE_PATH}/latest/apply', methods=['POST'])
def apply_latest_injection():
  action_kod = 'nectar.action.apply_latest_vendor_injections'
  job_id = job_client.enqueue_action(action_kod)
  return jsonify(data=dict(job_id=job_id))
