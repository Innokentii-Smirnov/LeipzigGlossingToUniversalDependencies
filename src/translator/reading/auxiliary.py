from ..model.glossing.auxiliary import PUNCTUATION
from ..model.glossing.word import GlossedWord

def is_empty_or_comment(line: str) -> bool:
  """Determines whether a line of a file containing a glossed text is empty or comment.

  :param line: The line to inspect
  :return: True if the given line is empty or comment, False otherwise
  """
  return line == "" or line.startswith("#") or line.startswith("@")

def delete_punctuation(word: str) -> str:
  """Функция, которая убирает пунктуационные знаки в конце и в начале слов.
  """
  if (word != "") and (word != " "):
    word = word.strip(PUNCTUATION)
    return word
  else:
    return word

def construct_words(tokens: list[str], glosses: list[str]) -> list[GlossedWord]:
  stripped_tokens = map(delete_punctuation, tokens)
  stripped_glosses = map(delete_punctuation, glosses)
  words = [GlossedWord(form, gloss) for form, gloss in zip(stripped_tokens, stripped_glosses, strict=True)]
  return words

def format_line_number(line_number: str) -> str:
    if "_" not in line_number:
        sent_id = line_number
    else:
        # "To split" is an irregular verb. The simple past and past participle is "split".
        split_number = line_number.split("_")
        sent_id = "{0}-{1}".format(split_number[0], split_number[-1])
    return sent_id
