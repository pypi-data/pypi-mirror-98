import json
import traceback
from copy import deepcopy
from datetime import datetime
from typing import Dict, Any, Union, List, Optional

from inflection import underscore
from rq import get_current_job
from rq.job import Job
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils, consts
from kama_sdk.core.core.types import ActionStatusDict, ErrDict
from kama_sdk.core.telem import telem_man
from kama_sdk.model.base.model import Model


class ActionError(Exception):
  def __init__(self, **err_descriptor):
    err_descriptor['fatal'] = err_descriptor.get('fatal', False)
    self.err_descriptor = deepcopy(err_descriptor)
    super().__init__(err_descriptor.get('reason'))


class FatalActionError(ActionError):
  def __init__(self, **kwargs):
    kwargs['fatal'] = True
    super().__init__(**kwargs)


class Action(Model):

  def __init__(self, config: Dict, parent=None):
    super().__init__(config)
    self.status = 'idle'
    self.logs = []
    self.exception = None
    self.parent = parent

  @cached_property
  def event_vid(self):
    return utils.gen_uuid()

  @cached_property
  def parent_event_tmp_id(self):
    return self.get_prop(KEY_PARENT_EVENT_VID)

  def gen_backup_event_name(self):
    return underscore(self.title or self.__class__.__name__)

  def run(self, **kwargs) -> Any:
    self.set_running()
    try:
      outcome = self.perform(**kwargs)
    except Exception as err:
      self.exception = err
      outcome = None

    should_raise = False

    if self.exception:
      status = consts.neg
      if issubclass(self.exception.__class__, ActionError):
        err: ActionError = self.exception
        should_raise = err.err_descriptor.get('fatal')
      else:
        should_raise = True
    else:
      status = consts.pos

    self.set_status(status)
    self.handle_telem()

    if should_raise:
      raise self.exception
    else:
      if outcome is not None:
        if not issubclass(outcome.__class__, Dict):
          print(f"[action:{self.id()} ret is not Dict: {outcome}]")
      return outcome

  def run_safely(self):
    try:
      return self.run() or True
    except:
      return None

  def cleanup(self):
    pass

  def raise_error(self):
    pass

  def handle_telem(self):
    try:
      if telem_man.is_storage_ready():
        print(f"[kama_sdk::action] danger event_id and store_event")
        event_bundle = self.gen_telem_dict()
        insertion_result = telem_man.store_event(event_bundle)
        event_id = str(insertion_result.inserted_id)

        if self.exception and self.am_sub_action():
          err_dict = exception2err_dict(self.exception)
          err_dict['event_id'] = event_id
          telem_man.store_error(err_dict)
    except Exception:
      print(f"Telem save failed")
      print(traceback.format_exc())

  def am_sub_action(self) -> bool:
    return issubclass(self.parent.__class__, Action)

  def am_root(self):
    return not self.am_sub_action()

  def gen_telem_dict(self):
    return dict(
      _id=self.event_vid,
      type=ACTION_EVENT_TYPE,
      name=self.id() or self.gen_backup_event_name(),
      parent_virtual_id=self.parent_event_tmp_id,
      status=self.status,
      logs=self.logs,
      extras=self.telem_extras(),
      occurred_at=str(datetime.now())
    )

  def set_running(self):
    self.set_status(consts.rng)

  def set_positive(self):
    self.set_status(consts.pos)

  def set_negative(self):
    self.set_status(consts.neg)

  def set_status(self, status):
    assert status in consts.statuses
    self.status = status
    self.notify_job()

  def perform(self, **kwargs) -> Optional[Dict]:
    raise NotImplementedError

  def add_logs(self, new_logs: Optional[List[str]]) -> None:
    new_logs = new_logs or []
    self.logs = [*self.logs, *new_logs]

  def telem_extras(self) -> Dict:
    return {}

  def find_root(self) -> Optional:
    if self.am_root():
      return self
    elif self.parent and issubclass(self.parent.__class__, Action):
      return self.parent.find_root()
    else:
      return None

  def notify_job(self):
    job: Job = get_current_job()
    if job:
      action_root = self.find_root()
      if action_root:
        progress_bundle = action_root.serialize_progress()
        job.meta['progress'] = json.dumps(progress_bundle)
        job.save_meta()
      else:
        print(f"[action:{self.id}] danger root not found")

  def serialize_progress(self) -> ActionStatusDict:
    return dict(
      id=self.id(),
      title=self.title,
      info=self.info,
      status=self.status,
      sub_items=[],
      logs=self.logs,
      error=serialize_error(self.exception)
    )

  @cached_property
  def expected_run_args(self) -> List[str]:
    return self.get_prop(EXPECTED_RUN_ARGS_KEY, [])

  def default_error_type(self):
    return self.id()


def serialize_error(exception: Exception):
  if exception:
    if issubclass(exception.__class__, ActionError):
      # noinspection PyUnresolvedReferences
      bundle = exception.err_descriptor
      return dict(
        fatal=bundle.get('fatal', False),
        type=bundle.get('type', 'unknown_type'),
        reason=bundle.get('reason') or 'Unknown Reason',
        logs=bundle.get('logs', [])
      )
    else:
      return dict(
        fatal=True,
        type='internal_error',
        reason='Internal Error',
        logs=utils.exception2trace(exception)
      )
  else:
    return None


def exception2err_dict(exception: Union[Exception, ActionError]) -> ErrDict:
  if issubclass(exception.__class__, ActionError):
    action_error: ActionError = exception
    return action_error.err_descriptor
  else:
    return ErrDict(
      fatal=True,
      type='internal_error',
      logs=utils.exception2trace(exception)
    )


KEY_PARENT_EVENT_VID = 'parent_event_virtual_id'
KEY_PARENT_EVENT_ID = 'parent_event_id'
ACTION_EVENT_TYPE = 'action'
EXPECTED_RUN_ARGS_KEY = 'expects_run_args'
