from dataclasses import dataclass
from typing import Any, Optional
from io import TextIOBase

SENT_ATTRS = ['sent_id', 'text', 'text_ru']

@dataclass(frozen=True)
class RawSentence:
    sent_id: str
    text: str
    text_ru: str
    MISC: str
    has_formatting_issue: bool
    glossed_text: str

    def __str__(self) -> str:
        return '\n'.join([self.sent_id, self.text, self.text_ru, self.MISC])

    def print_as_conllu(self, file: Optional[TextIOBase] = None) -> None:
        for attr in SENT_ATTRS:
            print('#{0} = {1}'.format(attr, getattr(self, attr)), file=file)
        print('#MISC: {0}'.format(self.MISC), file=file)

    def to_dict(self, source: str) -> dict[str, Any]:
        return {
            'id': self.sent_id,
            'text': self.text,
            # Если здесь будет приставка, которая у нас выделяется в отдельный токен, то длина будет на 1 меньше, чем кол-во токенов
            'length': len(self.text.split()),
            'source': source,
            'sentence_tree': '-',
            'russian_text': self.text_ru,
            'miscellaneous': self.MISC,
        }

    @property
    def numeric_id(self) -> int:
        first_line_number = self.sent_id.split('-', 1)[0]
        if first_line_number.isdigit():
            return int(first_line_number)
        else:
            return 0
