from unit import Unit
from typing import Sequence
from merging import merge_clitic_and_verb, format_verb_object
from typing import TypeVar, Callable
T = TypeVar('T')

def process_elements[T](elements: list[T], make_unit: Callable[[T], Unit]) -> None:
  i = 0
  while i < len(elements):
    unit = make_unit(elements[i])
    if 'VERB' in unit.tag:
      format_verb_object(unit)
    elif i + 1 < len(elements):
      next_unit = make_unit(elements[i + 1])
      if 'Clitic=Yes' in unit.tag and 'VERB' in next_unit.tag:
        del elements[i]
        merge_clitic_and_verb(unit, next_unit)
    i += 1
