from dataclasses import dataclass
from .auxiliary import is_lat, is_cyr, preprocess_token
from ..ud.word import UDWord
from ...conversion.lemma_detection import lemmas_gram
from ...part_of_speech import define_pos_tag
from ...conversion.properties import get_feats
from ... import EMPTY_FIELD_MARKER, MORPHOSYNTACTIC_PROPERTY_SEPARATOR
from ...atr_val import prefixes as language_has_prefixes
from warnings import warn
from logging import getLogger
logger = getLogger(__name__)

@dataclass(order=True, frozen=True)
class GlossedWord:
    segmentation: str
    gloss: str

    def __str__(self) -> str:
        return '{0:25} {1}'.format(self.segmentation, self.gloss)

    @property
    def has_proclitic(self) -> bool:
        gloss = self.gloss
        first_tag = gloss.split("-")[0]
        return (any(is_lat(char) for char in first_tag) and
                # Добавлено, чтобы не выделять хваршинские основы как проклитики
                not any(is_cyr(char) for char in first_tag) and
                len(gloss.split("-")) > 1 and
                any(is_cyr(char) for char in gloss))

    def to_UD_words(self, word_id: int=0) -> list[UDWord]:
        segmentation = self.segmentation
        gloss = self.gloss
        UD_words = list[UDWord]()
        try:
            lem1, gram1 = lemmas_gram(segmentation, gloss)
        except (IndexError, ValueError) as exc:
            warn('lemmas_gram raised\n{0}\non word "{1}" glossed as "{2}".'
                  .format(repr(exc), self.segmentation, self.gloss))
            logger.error('{0:30} {1}'.format(self.segmentation, self.gloss))
            lem1 = []
            gram1 = []
        lemma = lem1[0] if len(lem1) > 0 else 'None'
        upos_tag = define_pos_tag(lem1[1]) if len(lem1) > 0 else ["None"]
        feats, upos = get_feats(gram1, upos_tag)
        translation = lem1[1] if len(lem1) > 0 else 'None'
        if not language_has_prefixes and self.has_proclitic:
            clitic_form, segmented_word_form = segmentation.split("-", 1)
            clitic_lemma = clitic_form
            clitic_upos = "PART"
            clitic_feats = "Clitic=Yes"
            clitic_translation = gloss.split("-")[0]
            clitic = UDWord(str(word_id), clitic_form, clitic_lemma, clitic_upos, clitic_feats, clitic_translation)
            UD_words.append(clitic)
            word_id += 1
            word_form = preprocess_token(segmented_word_form)
        else:
            word_form = preprocess_token(segmentation)
        feats_string = MORPHOSYNTACTIC_PROPERTY_SEPARATOR.join(feats) if len(feats) > 0 else EMPTY_FIELD_MARKER
        word = UDWord(str(word_id), word_form, lemma, upos, feats_string, translation)
        UD_words.append(word)
        return UD_words
