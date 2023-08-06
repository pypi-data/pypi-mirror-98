import os
from os.path import isfile
from typing import Type, Optional, Dict, Union, List, TypeVar, Any

from werkzeug.utils import cached_property

from kama_sdk.core.core import utils, consts, subs2
from kama_sdk.core.core.types import KoD
from kama_sdk.model.base.default_models import default_model_classes

T = TypeVar('T', bound='Model')


class ModelsMan:
  def __init__(self):
    self._descriptors: List[Dict] = []
    self._classes: List[Type[T]] = []
    self._asset_paths: List[str] = []

  def add_descriptors(self, descriptors: List[Dict]):
    self._descriptors = self._descriptors + descriptors

  def add_classes(self, model_classes: List[Type[T]]):
    self._classes = self._classes + model_classes

  def add_asset_dir_paths(self, paths: List[str]):
    self._asset_paths += paths

  def add_defaults(self):
    self.add_descriptors(default_descriptors())
    self.add_classes(default_model_classes())
    self.add_asset_dir_paths(default_asset_paths())

  def clear(self, restore_defaults=True):
    self._descriptors = []
    self._classes = []
    if restore_defaults:
      self.add_defaults()

  def descriptors(self) -> List[Dict]:
    return self._descriptors

  def classes(self) -> List[Type[T]]:
    return self._classes

  def asset_dir_paths(self) -> List[str]:
    return self._asset_paths


models_man = ModelsMan()


class Model:

  def __init__(self, config: Dict):
    self.config: Dict = config
    self._id: str = config.get(ID_KEY)
    self.parent: Optional[T] = None
    self.reassign_props()
    self.config['kind'] = self.__class__.__name__

  def id(self) -> str:
    return self._id

  def reassign_props(self):
    transformations: Dict = self.get_prop('transform_props', {})
    if transformations:
      for (old_key, new_value) in transformations.items():
        self.config[old_key] = new_value

  def patch(self, new_props: Dict[str, any]):
    self.config = {**self.config, **new_props}

  @cached_property
  def title(self) -> str:
    return self.get_prop(TITLE_KEY)

  @cached_property
  def info(self) -> str:
    return self.get_prop(INFO_KEY)

  @cached_property
  def default_lookback(self) -> Union[int, bool]:
    return self.config.get('lookback', True)

  def to_dict(self):
    return dict(
      id=self.id(),
      title=self.title,
      info=self.info
    )

  def update_attrs(self, config: Dict):
    for key, value in config.items():
      setattr(self, key, value)

  def get_prop(self, key: str, backup: Any = None) -> Any:
    """
    Convenience method for resolve_props
    @param key: name of desired value in config dict
    @param backup: value to return if value not in config dict
    @return: fully resolved property value or backup if given
    """
    return self.resolve_prop(key, backup=backup)

  def resolve_prop(self, key: str, **kwargs) -> Any:
    """
    Reads a value from the main config dicts, applies all possible
    resolution transformations to obtain its final value. This includes
    1) IFTT resolution, 2) ValueSupplier resolution, and
    3) string substitutions.
    @param key:
    @param kwargs:
    @return: fully resolved property value or backup if given
    """
    depth = kwargs.pop('depth', None)
    if key in list(self.config.keys()):
      value = self.config[key]
    else:
      lookback = self.lookback2int(kwargs.pop('lookback', None))
      if self.parent and lookback > 0:
        parent_value = self.parent.resolve_prop(key, lookback=lookback-1)
        if parent_value:
          return parent_value

      lazy_backup = kwargs.pop('lazy_backup', None)
      if lazy_backup is not None:
        value = lazy_backup()
      elif 'backup' in kwargs.keys():
        value = kwargs.pop('backup', None)
      else:
        value = None
      if kwargs.get('warn'):
        print(f"[kama_sdk:{self.__class__.__name__}] undefined prop '{key}'")

    return self.resolve_prop_value(value, depth)

  def resolve_prop_value(self, value: Any, depth=0):
    if type(value) == str:
      value = self.supplier_resolve_or_identity(value)
      value = self.interpolate_prop(value)
      return self.try_read_from_asset(value)
    elif type(value) == list:
      return [self.resolve_prop_value(v) for v in value]
    elif type(value) == dict:
      txd_value = self.supplier_resolve_or_identity(value)
      if type(txd_value) == dict and int(depth or 0) > 0:
        perf = lambda v: self.resolve_prop_value(v, depth - 1)
        return {k: perf(v) for (k, v) in txd_value.items()}
      else:
        return txd_value
    else:
      return value

  def interpolate_prop(self, value: str) -> Any:
    """
    Performs string substitutions on input. Combines substitution context
    from instance's self.context and any additional context passed as
    parameters. Returns unchanged input if property is not a string.
    @param value: value of property to interpolate
    @return: interpolated string if input is string else unchanged input
    """
    if value and type(value) == str:
      def resolve(expr: str):
        ret = self.supplier_resolve_or_identity(expr)
        return str(ret) if ret else ''
      return subs2.interp(value, resolve)
    else:
      return value

  @classmethod
  def singleton_id(cls):
    raise NotImplemented

  @classmethod
  def inflate_singleton(cls, **kwargs) -> T:
    return cls.inflate_with_id(cls.singleton_id(), **kwargs)

  @classmethod
  def kind(cls):
    return cls.__name__

  def serialize(self) -> Dict:
    src_items = list(self.config.items())
    return {k: v for k, v in src_items}

  def inflate_children(self, child_class: Type[T], **kwargs):
    """
    Bottleneck function for a parent model to inflate a list of children.
    In the normal case, kods_or_provider_kod is a list of WizModels KoDs.
    In the special case, kods_or_provider_kod is ListGetter model
    that produces the actual children.
    case,
    @param child_class: class all children must a subclass of
    @return: resolved list of WizModel children
    """
    kods_or_supplier: Union[List[KoD], KoD] = kwargs.pop('kod', None)
    if kods_or_supplier is None:
      prop = kwargs.pop('prop', None)
      kods_or_supplier = self.config.get(prop) or []

    kods_or_supplier = kods_or_supplier or []
    to_child = lambda obj: self.kod2child(obj, child_class, **kwargs)

    if type(kods_or_supplier) == list:
      children_kods = kods_or_supplier
      return list(map(to_child, children_kods))
    elif type(kods_or_supplier) in [str, dict]:
      from kama_sdk.model.supplier.base.supplier import Supplier
      children_kods = self.supplier_resolve_or_identity(kods_or_supplier)
      if type(children_kods) == list:
        return list(map(to_child, children_kods))
      else:
        err = f"children must be list or supplier not {kods_or_supplier}"
        raise RuntimeError(f"[Model] {err}")

  def inflate_list_child(self, child_cls: Type[T], **kwargs) -> Optional[T]:
    prop = self.config.get(kwargs.pop('prop', None))
    list_kod: KoD = kwargs.pop('kod', prop)
    child_id: str = kwargs.pop('id', None)

    predicate = lambda obj: key_or_dict_matches(obj, child_id)
    child_kod = next((obj for obj in list_kod if predicate(obj)), None)
    if child_kod:
      return self.inflate_child(child_cls, kod=child_kod, **kwargs)
    else:
      return None

  def inflate_child(self, child_cls: Type[T], **kwargs) -> Optional[T]:
    prop = self.config.get(kwargs.pop('prop', None))
    kod: KoD = kwargs.pop('kod', prop)
    return self.kod2child(kod, child_cls, **kwargs)

  def kod2child(self, kod: KoD, child_cls: Type[T], **kwargs) -> T:
    if kwargs.get('resolve_kod', True):
      resolved_kod = self.supplier_resolve_or_identity(kod, **kwargs)
    else:
      resolved_kod = kod

    inflated = child_cls.inflate(resolved_kod, **kwargs)
    if inflated:
      inflated.parent = self
    return inflated

  def prop_inheritance_pool(self):
    return self.config

  def lookback2int(self, lookback_override: Union[bool, int]) -> int:
    overridden = lookback_override is not None
    lookback = lookback_override if overridden else self.default_lookback
    if type(lookback) == int:
      return lookback
    else:
      return 1000 if lookback else 0

  @classmethod
  def inflate_all(cls, **kwargs) -> List[T]:
    cls_pool = cls.lteq_classes(models_man.classes())
    configs = configs_for_kinds(models_man.descriptors(), cls_pool)
    return [cls.inflate(config, **kwargs) for config in configs]

  @classmethod
  def inflate(cls: T, kod: KoD, **kwargs) -> Optional[T]:
    try:
      if isinstance(kod, str):
        return cls.inflate_with_id(kod, **kwargs)
      elif isinstance(kod, Dict):
        return cls.inflate_with_config(kod, **kwargs)
      else:
        raise RuntimeError(f"Bad input {kod}")
    except Exception as err:
      if kwargs.pop('safely', False):
        return None
      else:
        print(f"[kama_sdk:{cls.kind()}] inflation error below for {kod}")
        raise err

  @classmethod
  def inflate_with_id(cls, _id: str, **kwargs) -> T:
    if _id and _id[0] and _id[0].isupper():
      config = dict(kind=_id)
    else:
      candidate_subclasses = cls.lteq_classes(models_man.classes())
      candidate_kinds = [klass.kind() for klass in candidate_subclasses]
      all_configs = models_man.descriptors()
      config = find_config_by_id(_id, all_configs, candidate_kinds)
    return cls.inflate_with_config(config, **kwargs)

  @classmethod
  def descendent_or_self(cls) -> T:
    subclasses = cls.lteq_classes(models_man.classes())
    not_self = lambda kls: not kls == cls
    return next(filter(not_self, subclasses), cls)({})

  @classmethod
  def inflate_with_config(cls, config: Dict, **kwargs) -> T:
    patches: Optional[Dict] = kwargs.get('patches', {})

    host_class = cls

    inherit_id = config.get(INHERIT_KEY)
    explicit_kind = config.get(KIND_KEY)

    if explicit_kind and not explicit_kind == host_class.__name__:
      host_class = cls.kind2cls(explicit_kind)
      if not host_class:
        err = f"no kind {explicit_kind} under {cls.__name__}"
        raise RuntimeError(f"[Model] FATAL {err}")

    if inherit_id:
      other = cls.inflate_with_id(inherit_id, **kwargs)
      host_class = other.__class__
      config = {**other.config, **config}

    final_config = utils.deep_merge(config, patches)
    model_instance = host_class(final_config)

    return model_instance

  def supplier_resolve_or_identity(self, kod: KoD, **kwargs) -> Any:
    from kama_sdk.model.supplier.base.supplier import Supplier
    prefix: str = "get::"

    if self.is_interceptor_candidate(Supplier, prefix, kod):
      final_kod = kod
      if type(kod) == str:
        trimmed_kod = kod.replace(prefix, "")
        final_kod = Supplier.expr2props(trimmed_kod)

      kwargs.pop('safely', None)
      interceptor = Supplier.inflate(
        final_kod,
        safely=True,
        **kwargs
      )
      if interceptor:
        interceptor.parent = self
        return interceptor.resolve()

    return kod

  @classmethod
  def id_exists(cls, _id: str) -> bool:
    return True

  @staticmethod
  def truncate_kod_prefix(kod: KoD, prefix: str) -> KoD:
    if type(kod) == str and len(kod) >= len(prefix):
      return kod[len(prefix):len(kod)]
    return kod

  @classmethod
  def is_interceptor_candidate(cls, interceptor: Type[T], prefix, kod: KoD):
    if type(kod) == dict:
      interceptors = interceptor.lteq_classes(models_man.classes())
      if kod.get('kind') in [c.__name__ for c in interceptors]:
        return True
    if type(kod) == str:
      return kod.startswith(prefix)
    return False

  @classmethod
  def lteq_classes(cls, classes: List[Type]) -> List[Type[T]]:
    return [klass for klass in [*classes, cls] if issubclass(klass, cls)]

  @classmethod
  def kind2cls(cls, kind: str):
    subclasses = cls.lteq_classes(models_man.classes())
    return find_class_by_name(kind, subclasses)

  @staticmethod
  def try_read_from_asset(value):
    if value and type(value) == str:
      if value.startswith(ASSET_PREFIX):
        return read_from_asset(value)
    return value


def read_from_asset(descriptor: str) -> str:
  _, path = descriptor.split("::")
  for dirpath in models_man.asset_dir_paths():
    full_path = f"{dirpath}/{path}"
    if isfile(full_path):
      with open(full_path) as file:
        return file.read()
  return ''


def key_or_dict_to_key(key_or_dict: Union[str, dict]) -> str:
  if isinstance(key_or_dict, str):
    return key_or_dict
  elif isinstance(key_or_dict, dict):
    return key_or_dict.get('id')
  raise RuntimeError(f"Can't handle {key_or_dict}")


def key_or_dict_matches(key_or_dict: KoD, target_key: str) -> bool:
  return key_or_dict_to_key(key_or_dict) == target_key


def find_class_by_name(name: str, classes) -> Type:
  matcher = lambda klass: klass.__name__ == name
  return next(filter(matcher, classes), None)


def find_config_by_id(_id: str, configs: List[Dict], kinds: List[str]) -> Dict:
  matcher = lambda c: c.get('id') == _id and c.get('kind') in kinds
  return next(filter(matcher, configs), None)


def configs_for_kinds(configs: List[Dict], cls_pool) -> List[Dict]:
  kinds_pool = [cls.__name__ for cls in cls_pool]
  return [c for c in configs if c.get('kind') in kinds_pool]


def default_descriptors() -> List[Dict]:
  pwd = os.path.join(os.path.dirname(__file__))
  search_space_root = f"{pwd}/../../model"
  yaml_dirs = discover_model_yaml_dirs(search_space_root)
  return utils.flatten(list(map(utils.yamls_in_dir, yaml_dirs)))


def discover_model_yaml_dirs(root: str) -> List[str]:
  pwd = root.split('/')[-1]
  is_root_yaml_dir = pwd == 'model_yamls'
  child_paths = [f"{root}/{name}" for name in os.listdir(root)]
  child_dirs = list(filter(os.path.isdir, child_paths))
  child_results = list(map(discover_model_yaml_dirs, child_dirs))
  self_result = [root] if is_root_yaml_dir else []
  return self_result + utils.flatten(child_results)


def default_asset_paths() -> List[str]:
  pwd = os.path.join(os.path.dirname(__file__))
  return [f"{pwd}/../../assets"]


ID_KEY = 'id'
TITLE_KEY = 'title'
INHERIT_KEY = 'inherit'
KIND_KEY = 'kind'
INFO_KEY = 'info'
ASSET_PREFIX = f'{consts.FILE_PREFIX}::'
