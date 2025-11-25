from dataclasses import dataclass
from ..raw.sentence import RawSentence
from .word import GlossedWord
from ..ud.sentence import UDSentence
from ..ud.word import UDWord
from contextvars import ContextVar
ctx_sent_id: ContextVar[str] = ContextVar('sent_id')
ctx_sent_id.set('Unknown line')
ctx_segmentation: ContextVar[str] = ContextVar('segmentation')
ctx_segmentation.set('Unknown segmentation')
ctx_gloss: ContextVar[str] = ContextVar('gloss')
ctx_gloss.set('Unknown gloss')

@dataclass(frozen=True)
class GlossedSentence:
    raw: RawSentence
    words: list[GlossedWord]

    def __str__(self):
        return '\n'.join([str(self.raw)] + [str(word) for word in self.words])

    def __iter__(self):
        return self.words.__iter__()

    def to_UD_sentence(self) -> UDSentence:
        raw = self.raw
        ctx_sent_id.set(raw.sent_id)
        UD_words = list[UDWord]()
        word_id = 1
        for glossed_word in self:
            ctx_segmentation.set(glossed_word.segmentation)
            ctx_gloss.set(glossed_word.gloss)
            current_UD_words = glossed_word.to_UD_words(word_id)
            word_id += len(current_UD_words)
            UD_words.extend(current_UD_words)
        return UDSentence(raw, UD_words)
