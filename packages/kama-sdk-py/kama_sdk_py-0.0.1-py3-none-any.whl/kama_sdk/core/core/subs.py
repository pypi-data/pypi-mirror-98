import re
from typing import Dict, Any

NON_DOT = "---"

class SubsGetter:
  def __init__(self, src: Dict):
    self.src: Dict = src

  def __getitem__(self, k: str):
    k = k.replace(NON_DOT, ".")
    resolver_desc = k.split("/")
    if k in self.src.keys():
      direct_hit = self.src.get(k)
      if callable(direct_hit):
        return direct_hit()
      else:
        return direct_hit
    elif len(resolver_desc) == 2:
      resolvers = self.src.get('resolvers', {})
      resolver = resolvers.get(resolver_desc[0])
      resolvable_key = resolver_desc[1]
      return resolver(resolvable_key) if resolver else None
    else:
      return None
  __getattr__ = __getitem__


def interp_dict_vals(root: Dict, context: Dict) -> Dict:
  new_dict = {}

  def do_sub(var: any) -> any:
    return interp_str(var, context) if type(var) == str else var

  for k, v in list(root.items()):
    if type(v) == dict:
      new_dict[k] = interp_dict_vals(v, context)
    elif type(v) == list:
      for i, item in v:
        if type(v) == dict:
          new_dict[k][i] = interp_dict_vals(item, context)
        else:
          new_dict[k][i] = do_sub(v)
    else:
      new_dict[k] = do_sub(v)
  return new_dict


def coerce_sub_tokens(string: str):
  pattern = re.compile(r"{(.*?)}")
  empty_exclude = lambda s: not s.strip() == ''
  matches = list(filter(empty_exclude, pattern.findall(string)))
  output = string
  for match in matches:
    replacement = '0.' + match.replace(".", NON_DOT)
    output = output.replace('{' + match + '}', '{' + replacement + '}')
  return output


def interp_any(string: str, context: Dict) -> Any:
  if type(string) == str:
    pattern = re.compile(r"{(.*?)}")
    empty_exclude = lambda s: not s.strip() == ''
    matches = list(filter(empty_exclude, pattern.findall(string)))
    if len(matches) == 1:
      key = matches[0]
      return SubsGetter(context).__getitem__(key)
    else:
      return string
  else:
    return string


def interp_str(value: Any, context: Dict) -> Any:
  if type(value) == str:
    fmt_string = coerce_sub_tokens(value)
    actual = fmt_string.format(SubsGetter(context or {}))
    actual = None if actual == 'None' else actual
    return actual
  else:
    return value
