from typing import Dict

from flask import Blueprint, jsonify, request

from kama_sdk.controllers.ctrl_utils import jparse
from kama_sdk.core.core import job_client, utils, consts
from kama_sdk.core.telem import telem_man
from kama_sdk.model.operation.operation import Operation
from kama_sdk.model.operation.operation_state import OperationState, operation_states
from kama_sdk.model.operation.stage import Stage
from kama_sdk.model.operation.step import Step
from kama_sdk.serializers import operation_serial as operation_serial, step_serial

OPERATIONS_PATH = '/api/operations'
OPERATION_PATH = f'/{OPERATIONS_PATH}/<operation_id>'

STAGES_PATH = f'{OPERATION_PATH}/stages'
STAGE_PATH = f'{STAGES_PATH}/<stage_id>'

STEPS_PATH = f'{STAGE_PATH}/steps'
STEP_PATH = f'{STEPS_PATH}/<step_id>'

FIELDS_PATH = f'{STEP_PATH}/fields'
FIELD_PATH = f'{FIELDS_PATH}/<field_id>'

controller = Blueprint('operations_controller', __name__)


@controller.route(OPERATIONS_PATH)
def operations_index():
  """
  Lists all existing Operations for a local app, except system ones.
  :return: list of minimally serialized Operation objects.
  """
  all_ops = Operation.inflate_all()
  operations_list = [op for op in all_ops if not op.is_system()]
  dicts = [operation_serial.ser_standard(c) for c in operations_list]
  return jsonify(data=dicts)


@controller.route(OPERATION_PATH)
def operations_show(operation_id):
  """
  Finds and returns a particular Operation using operation_id.
  :param operation_id: operation id to search by.
  :return: fully serialized Operation object.
  """
  operation = find_operation(operation_id)
  return jsonify(data=operation_serial.ser_full(operation))


@controller.route(f'{OPERATIONS_PATH}/osts')
def operations_ost_index():
  """
  Generates a list of currently available OperationStates.
  :return: list of currently available OperationStates.
  """
  return jsonify(data=operation_states)


@controller.route(f'{OPERATION_PATH}/generate-ost', methods=['POST'])
def operations_gen_ost(operation_id):
  """
  Generates a new OST (random 10 character string).
  :return: new OST.
  """
  uuid = OperationState.gen(operation_id)
  return jsonify(data=uuid)


@controller.route(f"{OPERATION_PATH}/eval-preflight", methods=['POST'])
def eval_preflight(operation_id):
  """
  Finds the Prerequisite with a matching operation_id and prerequisite_id,
  and evaluates it.
  :param operation_id: operation id to search by.
  :return: dict containing results of evaluation.
  """
  operation = find_operation(operation_id)
  action_kod = operation.preflight_action_kod
  if action_kod:
    job_id = job_client.enqueue_action(action_kod)
    return jsonify(data=dict(job_id=job_id))
  else:
    return jsonify(data=dict(job_id=None))


@controller.route(f"{STEP_PATH}/refresh", methods=['POST'])
def step_refresh(operation_id, stage_id, step_id):
  """
  Finds the Step with a matching operation_id, stage_id and step_id.
  :param operation_id: operation id to search by.
  :param stage_id: stage id to search by.
  :param step_id: step id to search by.
  :return: serialized Step object.
  """
  values: Dict = utils.flat2deep(jparse()['values'])
  op_state = find_op_state(operation_id=operation_id)
  step = find_step(operation_id, stage_id, step_id)
  find_op_state().gen_step_state(step, keep=False)
  asgs = step.partition_vars(values, op_state)
  serialized = step_serial.ser_refreshed(step, values, op_state)
  return jsonify(data=dict(
    step=serialized,
    manifest_assignments=asgs.get(consts.TARGET_STANDARD)
  ))


@controller.route(f"{STEP_PATH}/preview-chart-assignments", methods=['POST'])
def step_preview_chart_assigns(operation_id, stage_id, step_id):
  """
  Returns the chart assignments that would be committed if the step were submitted
  with current user input.
  :param operation_id: operation id used to locate the right step
  :param stage_id: stage id used to locate the right step
  :param step_id: step id used to locate the right step
  :return: dictionary with chart assigns.
  """
  values = utils.flat2deep(jparse()['values'])
  op_state = find_op_state(operation_id=operation_id)
  step = find_step(operation_id, stage_id, step_id)
  op_state.gen_step_state(step, keep=False)
  asgs = step.partition_vars(values, op_state)
  return jsonify(data=asgs[consts.TARGET_STANDARD])


@controller.route(f"{STEP_PATH}/run", methods=['POST'])
def step_run(operation_id, stage_id, step_id):
  """
  Submits a step. This includes:
    1. Finding the appropriate OperationState
    2. Appending a new StepState to OperationState
    3. Committing the step (See docs for step commit)
    4. Updating the StepState with the details of the commit outcome
  :param operation_id: operation id to search by.
  :param stage_id: stage id to search by.
  :param step_id: step id to search by.
  :return: dict containing submit status, message and logs.
  """
  values = utils.flat2deep(jparse()['values'])
  step = find_step(operation_id, stage_id, step_id)
  op_state = find_op_state(operation_id=operation_id)
  step_state = op_state.gen_step_state(step)
  job_id = step.run(values, step_state)
  return jsonify(data=dict(job_id=job_id))


@controller.route(f'{STEP_PATH}/next')
def steps_next_id(operation_id, stage_id, step_id):
  """
  computes and returns the id of the next step.
  :param operation_id: operation id to locate the right step.
  :param stage_id: stage id to locate the right step.
  :param step_id: step id to locate the right step.
  :return: computed id of next step or "done" if no more steps left.
  """
  stage = find_stage(operation_id, stage_id)
  step = find_step(operation_id, stage_id, step_id)
  op_state = find_op_state()
  result = stage.next_step_id(step, op_state)
  return jsonify(step_id=result)


@controller.route(f'{FIELD_PATH}/validate', methods=['POST'])
def step_field_validate(operation_id, stage_id, step_id, field_id):
  value = jparse()['value']
  step = find_step(operation_id, stage_id, step_id)
  op_state = find_op_state(operation_id=operation_id)
  eval_result = step.validate_field(field_id, value, op_state)
  status = 'valid' if eval_result['met'] else eval_result['tone']
  message = None if eval_result['met'] else eval_result['reason']
  return jsonify(data=dict(status=status, message=message))


@controller.route(f'{OPERATIONS_PATH}/mark-finished', methods=['POST'])
def operation_mark_finished():
  """
  Syncs telemetry information with the database if permissions allow to do so.
  Deletes OperationState after its done.
  :return: success or failure status depending if managed to find and delete
  the appropriate operation.
  """
  status = jparse().get('status', 'positive')
  operation_state = find_op_state()
  operation_state.notify_ended(status)
  event_telem = operation_state.gen_event_telem()
  telem_man.store_event(event_telem)
  return jsonify(data=dict(success='yeah'))


def find_operation(operation_id: str) -> Operation:
  """
  Inflates (instantiates) an instance of an Operation by operation_id.
  :param operation_id: desired operation to be inflated.
  :return: Operation instance.
  """
  return Operation.inflate(operation_id)


def find_stage(operation_id, stage_id) -> Stage:
  """
  Finds the Stage with a matching operation_id and stage_id.
  :param operation_id: operation id to search by.
  :param stage_id: stage id to search by.
  :return: Stage class instance.
  """
  operation = find_operation(operation_id)
  return operation.stage(stage_id)


def find_step(operation_id, stage_id, step_id) -> Step:
  """
  Finds the Step with a matching operation_id, stage_id and step_id.
  :param operation_id: operation id to search by.
  :param stage_id: stage id to search by.
  :param step_id: step id to search by.
  :return: Step class instance.
  """
  stage = find_stage(operation_id, stage_id)
  return stage.step(step_id)


def find_op_state(**kwargs) -> OperationState:
  op_id = kwargs.get('operation_id')
  raise_on_fail = kwargs.get('raise_on_fail', True)

  token = request.headers.get('Ostid')
  op_state = OperationState.find(token) if token else None

  if not op_state:
    if utils.is_in_cluster():
      if raise_on_fail:
        raise RuntimeError('OST ID not provided in headers!')
    else:
      uuid = OperationState.gen(op_id)
      op_state = OperationState.find(uuid)

  return op_state
