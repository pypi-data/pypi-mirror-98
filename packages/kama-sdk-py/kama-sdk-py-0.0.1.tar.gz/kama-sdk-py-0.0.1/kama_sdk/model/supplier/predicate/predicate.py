from typing import Dict, Any, Optional

from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.model.supplier.base.supplier import Supplier


class Predicate(Supplier):

  @property   # caching it breaks status_computer's logic. need
  def challenge(self) -> Any:
    # we need a new @wiz_property with custom caching logic
    return self.resolve_prop(CHALLENGE_KEY, warn=True)

  @cached_property
  def check_against(self) -> Optional[Any]:
    return self.resolve_prop(CHECK_AGAINST_KEY, warn=True)

  @cached_property
  def operator(self) -> str:
    return self.get_prop(OPERATOR_KEY, '==')

  @cached_property
  def is_optimist(self) -> bool:
    return self.get_prop(CASCADES_FAILURE, False)

  @property
  def is_pessimist(self) -> bool:
    return not self.is_optimist

  @cached_property
  def tone(self) -> str:
    return self.get_prop(TONE_KEY, 'error')

  @cached_property
  def reason(self) -> str:
    return self.get_prop(REASON_KEY, '')

  def resolve(self) -> bool:
    # print(f"Compare {self.challenge} {self.operator} {self.check_against}")
    return self.perform_comparison(
      self.operator,
      self.challenge,
      self.check_against
    )

  def error_extras(self) -> Dict:
    return dict(
      predicate_id=self.id(),
      predicate_kind=self.kind()
    )

  def culprit_res_signature(self) -> Dict:
    return self.get_prop(BLAME_RES_SIG)

  # noinspection PyBroadException
  @staticmethod
  def perform_comparison(_name: str, challenge: Any, against: Any) -> bool:
    challenge = utils.unmuck_primitives(challenge)
    against = utils.unmuck_primitives(against)

    try:
      if _name in ['equals', 'equal', 'eq', '==', '=']:
        return challenge == against

      elif _name in ['not-equals', 'not-equal', 'neq', '!=', '=/=']:
        return not challenge == against

      elif _name in ['is-in', 'in']:
        return challenge in undefined_alias(against)

      elif _name in ['contains']:
        return against in undefined_alias(challenge)

      elif _name in ['only', 'contains-only']:
        return set(challenge) == {against}

      elif _name in ['is-greater-than', 'greater-than', 'gt', '>']:
        return challenge > against

      elif _name in ['gte', '>=']:
        return challenge >= against

      elif _name in ['is-less-than', 'less-than', 'lt', '<']:
        return challenge < against

      elif _name in ['lte', '<=']:
        return challenge <= against

      elif _name in ['presence', 'defined', 'is-defined']:
        return bool(challenge)

      elif _name in ['undefined', 'is-undefined']:
        return not challenge

      print(f"Don't know operator {_name}")
      return False
    except:
      return False


def undefined_alias(values):
  if type(values) == list:
    new_list = []
    for value in values or []:
      if not value:
        new_list.append('__undefined__')
      new_list.append(value)
    return new_list
  else:
    return values


CHALLENGE_KEY = 'challenge'
OPERATOR_KEY = 'operator'
CHECK_AGAINST_KEY = 'check_against'
TONE_KEY = 'tone'
REASON_KEY = 'reason'
BLAME_RES_SIG = 'culprit_resource_signature'
CASCADES_FAILURE = 'optimistic'
TAGS = 'tags'
