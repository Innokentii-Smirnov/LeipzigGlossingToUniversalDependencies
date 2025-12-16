from unit import Unit
from type_definition import ConstituentDict

class Constituent(Unit):

  def __init__(self, dict: ConstituentDict):
    self.dict = dict

  @property
  def tag(self) -> list[str]:
    return self.dict['tags']

  @tag.setter
  def tag(self, value: list[str]) -> None:
    self.dict['tags'] = value

  @property
  def form(self) -> str:
    return self.dict['text']

  @form.setter
  def form(self, value: str) -> None:
    self.dict['text'] = value
