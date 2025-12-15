from formatting import format_verb_feats, get_formatted_clitic_agr_feats
from type_definition import Token

def merge_clitic_and_verb(clitic: Token, verb: Token) -> None:
  clitic_agr_feats = get_formatted_clitic_agr_feats(clitic)
  verb_feats = format_verb_feats(verb)
  verb['tagsets'][0] = [verb_feats[0]] + clitic_agr_feats + verb_feats[1:]
  verb['token'] = clitic['token'] + verb['token']

def format_verb_object(verb: Token) -> None:
  verb_feats = format_verb_feats(verb)
  verb['tagsets'][0] = verb_feats
