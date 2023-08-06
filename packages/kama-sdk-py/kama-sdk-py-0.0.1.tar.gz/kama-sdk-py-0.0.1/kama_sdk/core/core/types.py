from typing import Optional, Dict, List, Union

from typing_extensions import TypedDict


class InjectionsDesc(TypedDict):
  standard: Dict
  inline: Dict


class TemplateArgs(TypedDict, total=False):
  flat_inlines: Dict
  values: Dict


class ActionStatusDict(TypedDict, total=False):
  id: Optional[str]
  title: str
  info: Optional[str]
  status: str
  sub_items: List['ActionStatusDict']
  data: Dict
  error: Dict
  error_id: str
  logs: List[str]


class TimeSeriesDataPoint(TypedDict):
  timestamp: str
  value: float


class EndpointDict(TypedDict):
  name: str
  url: Optional[str]
  type: str
  online: bool
  svc_type: Optional[str]


class UpdateDict(TypedDict):
  id: str
  version: str
  ktea_type: Optional[str]
  ktea_uri: Optional[str]
  note: str


class JobStatusPart(TypedDict):
  name: str
  status: str
  pct: Optional[int]


class JobStatus(TypedDict):
  parts: List[JobStatusPart]
  logs: List[str]


class PredEval(TypedDict, total=False):
  predicate_id: str
  name: str
  met: bool
  reason: Optional[str]
  tone: str


class ExitStatuses(TypedDict, total=False):
  positive: List[PredEval]
  negative: List[PredEval]


class CommitOutcome(TypedDict, total=False):
  status: str
  reason: Optional[str]
  logs: List[str]


class K8sResMeta(TypedDict):
  namespace: str
  name: str


class K8sResDict(TypedDict):
  kind: str
  metadata: K8sResMeta


class KteaDict(TypedDict, total=False):
  type: str
  uri: str
  args: Optional[str]
  version: str
  weak_merge: Optional[Dict]
  strong_merge: Optional[Dict]


class KamaDict(TypedDict, total=False):
  type: str
  uri: str
  version: str


class ConfigBackup(TypedDict, total=False):
  event_id: str
  timestamp: str
  data: Dict


class ActionOutcome(TypedDict):
  cls_name: str
  id: str
  charge: str
  data: Dict


class StepActionKwargs(TypedDict):
  inline_assigns: Dict
  chart_assigns: Dict
  state_assigns: Dict


class KAO(TypedDict):
  api_group: Optional[str]
  kind: str
  name: str
  verb: Optional[str]
  error: Optional[str]


class ErrDict(TypedDict, total=False):
  uuid: str
  event_vid: Optional[str]
  event_id: Optional[str]
  type: str
  fatal: bool
  logs: List[str]
  reason: str
  resource: Dict
  extras: Dict


KAOs = List[KAO]
KoD = Union[str, dict]
KDLoS = Union[str, dict]
