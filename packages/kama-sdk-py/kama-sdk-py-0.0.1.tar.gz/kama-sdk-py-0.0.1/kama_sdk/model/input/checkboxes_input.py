from typing import Optional, Any

from kama_sdk.model.input.generic_input import GenericInput


class CheckboxesInput(GenericInput):
  pass

class CheckboxInput(GenericInput):
  def compute_inferred_default(self) -> Optional[Any]:
    return False


class SelectInput(GenericInput):
  pass
