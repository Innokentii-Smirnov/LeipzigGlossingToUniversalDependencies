from typing import TypedDict

class TokenDict(TypedDict):
  tagsets: list[list[str]]
  token: str

class ConstituentDict(TypedDict):
  tags: list[str]
  text: str
  tokens: list[list[str]]
