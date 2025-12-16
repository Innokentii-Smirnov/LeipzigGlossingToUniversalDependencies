from unit import Unit
from type_definition import UnitDict

class Token(Unit):

  def __init__(self, dict: UnitDict):
    self.dict = dict

  @property
  def tag(self) -> list[str]:
    assert isinstance(self.dict['tagsets'], list)
    return self.dict['tagsets'][0]

  @tag.setter
  def tag(self, value: list[str]) -> None:
    assert isinstance(self.dict['tagsets'], list)
    self.dict['tagsets'][0] = value

  @property
  def form(self) -> str:
    assert isinstance(self.dict['token'], str)
    return self.dict['token']

  @form.setter
  def form(self, value: str) -> None:
    assert isinstance(self.dict['token'], str)
    self.dict['token'] = value
