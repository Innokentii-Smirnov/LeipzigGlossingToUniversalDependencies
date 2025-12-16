from formatting import format_verb_feats, get_formatted_clitic_agr_feats
from unit import Unit

def merge_clitic_and_verb(clitic: Unit, verb: Unit) -> None:
  clitic_agr_feats = get_formatted_clitic_agr_feats(clitic)
  verb_feats = format_verb_feats(verb)
  verb.tag = [verb_feats[0]] + clitic_agr_feats + verb_feats[1:]
  verb.form = clitic.form + verb.form

def format_verb_object(verb: Unit) -> None:
  verb_feats = format_verb_feats(verb)
  verb.tag = verb_feats
