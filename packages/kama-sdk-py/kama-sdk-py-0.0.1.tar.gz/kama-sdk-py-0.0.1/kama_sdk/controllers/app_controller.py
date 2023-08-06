from flask import Blueprint, jsonify

from kama_sdk.core.core import job_client
from kama_sdk.core.telem import telem_man
from kama_sdk.model.adapters.app_status_computer import AppStatusComputer
from kama_sdk.model.adapters.deletion_spec import DeletionSpec
from kama_sdk.model.glance.glance_descriptor import GlanceDescriptor
from kama_sdk.model.hook import hook_serial
from kama_sdk.model.hook.hook import Hook

controller = Blueprint('app_controller', __name__)

BASE_PATH = '/api/app'


@controller.route(f'{BASE_PATH}/compute-status', methods=['GET', 'POST'])
def run_status_compute():
  computer = AppStatusComputer.inflate_singleton()
  application_status = computer.compute_and_commit_status()
  return jsonify(app_status=application_status)


@controller.route(f'{BASE_PATH}/sync-hub', methods=['POST'])
def sync_hub():
  job_id = job_client.enqueue_func(telem_man.upload_all_meta)
  return jsonify(job_id=job_id)


@controller.route(f'{BASE_PATH}/install-hooks')
def app_list_install_hooks():
  install_hooks = Hook.by_trigger(event='install')
  serialized_list = list(map(hook_serial.standard, install_hooks))
  return jsonify(data=serialized_list)


@controller.route(f'{BASE_PATH}/uninstall-hooks')
def app_list_uninstall_hooks():
  uninstall_hooks = Hook.by_trigger(event='uninstall')
  serialized_list = list(map(hook_serial.standard, uninstall_hooks))
  return jsonify(data=serialized_list)


@controller.route(f'{BASE_PATH}/uninstall-spec')
def uninstall_victims():
  del_spec: DeletionSpec = DeletionSpec.inflate('nectar.deletion-spec')
  return jsonify(data=del_spec.config)


@controller.route(f'{BASE_PATH}/deletion_selectors')
def deletion_selectors():
  deletion_map = 3
  return jsonify(data=deletion_map)


@controller.route(f'{BASE_PATH}/hooks/<hook_id>/run', methods=['POST'])
def run_hook(hook_id):
  hook = Hook.inflate(hook_id)
  action = hook.action()
  id_or_kind = action.id() or action.kind()
  job_id = job_client.enqueue_action(id_or_kind)
  return jsonify(data=dict(job_id=job_id))


@controller.route(f'{BASE_PATH}/jobs/<job_id>/status')
def job_progress(job_id):
  status_wrapper = job_client.job_status(job_id)
  return jsonify(
    data=dict(
      status=status_wrapper.status(),
      progress=status_wrapper.progress_bundle,
      result=status_wrapper.result
    )
  )


@controller.route(f'{BASE_PATH}/glance-ids', methods=["GET"])
def glance_ids():
  """
  Returns a list of application endpoint adapters.
  :return: list of serialized adapters.
  """
  glances = GlanceDescriptor.inflate_all()
  serialized = list(map(GlanceDescriptor.fast_serialize, glances))
  return jsonify(data=serialized)


@controller.route(f'{BASE_PATH}/glances/<glance_id>', methods=["GET"])
def get_glance(glance_id: str):
  glance = GlanceDescriptor.inflate(glance_id)
  return jsonify(data=glance.compute_and_serialize())
