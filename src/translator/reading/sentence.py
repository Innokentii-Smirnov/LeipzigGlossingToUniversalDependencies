import re
import warnings
from io import TextIOBase, StringIO
from .. import EMPTY_FIELD_MARKER
from ..model.raw.sentence import RawSentence
from ..model.glossing.sentence import GlossedSentence
from ..model.glossing.word import GlossedWord
from ..model.glossing.auxiliary import preprocess_token
from .tokenizer import Tokenizer
from .attribution_remover import AttributionRemover
from .token_filter import TokenFilter
from .auxiliary import is_empty_or_comment, format_line_number, construct_words
WARNING_PREFIX = '# WARNING: '

def read_sentence_from_stream(stream: TextIOBase) -> GlossedSentence | None:
    """Reads the first glossed sentence from a text stream

    :param stream: A text stream yielding the liens of a glossed text one by one
    :raises ValueError: No translation was given for the glossed sentence
    :return: A Sentence object representing the first glossed sentence if there are any glossed sentences in the file, None otherwise
    """
    sentence_words = list[GlossedWord]()
    # The tokens in the following variable should preserve trailing punctuation.
    sentence_tokens = list[str]()
    # The next variable stores the tokens of the current line.
    line_tokens: list[str] | None = None
    # We need this variable outside of the loop for error messages.
    line_id = "unknown"
    # To print the glossed sentence to the skipped sentences file if it has a formatting issue
    glossed_text = StringIO()
    has_formatting_issue = False
    for line in stream:
        line = line.strip()
        if not line.startswith(WARNING_PREFIX):
            print(line, file=glossed_text)
        if not is_empty_or_comment(line):
            split = re.split("\t| ", line, 1)
            if len(split) < 2:
              has_formatting_issue = True
              message = "A line is not numbered: {0}".format(line)
              warnings.warn(message)
              print(WARNING_PREFIX + message, file=glossed_text)
              continue
            line_id, line_body = split
            line_number = line_id[0:-1]
            line_type = line_id[-1]
            if line_number[0].isdigit():
                match line_type:
                    # Token line
                    case ">":
                        line_tokens = Tokenizer.tokenize(line)[1:]
                        unsegmented_line_tokens = [preprocess_token(token) for token in line_tokens]
                        sentence_tokens.extend(unsegmented_line_tokens)
                        line_tokens = AttributionRemover.remove_attribution(line_tokens)
                        line_tokens = TokenFilter.filter_tokens(line_tokens)
                    # Gloss line
                    case "<":
                        glosses = Tokenizer.tokenize(line)[1:]
                        glosses = AttributionRemover.remove_attribution(glosses)
                        if line_tokens is None:
                            has_formatting_issue = True
                            print(WARNING_PREFIX + "The gloss line {0} has no corresponding token line.".format(line_id),
                                  file=glossed_text)
                            line_tokens = [EMPTY_FIELD_MARKER] * len(glosses)
                        elif len(glosses) < len(line_tokens):
                            has_formatting_issue = True
                            print(WARNING_PREFIX + "The gloss line {0} has fewer tokens than the corresponding token line.".format(line_id),
                                  file=glossed_text)
                            glosses = [EMPTY_FIELD_MARKER] * len(line_tokens)
                        elif len(glosses) > len(line_tokens):
                            has_formatting_issue = True
                            print(WARNING_PREFIX + "The gloss line {0} has more tokens than the corresponding token line.".format(line_id),
                                  file=glossed_text)
                            glosses = [EMPTY_FIELD_MARKER] * len(line_tokens)
                        line_words = construct_words(line_tokens, glosses)
                        sentence_words.extend(line_words)
                    # Translation line
                    case "=":
                        sent_id = format_line_number(line_number)
                        text = " ".join(sentence_tokens)
                        text_ru = line_body.strip()
                        MISC = ""
                        raw_sentence = RawSentence(sent_id, text, text_ru, MISC, has_formatting_issue, glossed_text.getvalue())
                        return GlossedSentence(raw_sentence, sentence_words)

    if (len(sentence_words) == 0):
        return None
    else:
        raise ValueError("No translation was provided for the sentence ending on line {0}".format(line_id))
