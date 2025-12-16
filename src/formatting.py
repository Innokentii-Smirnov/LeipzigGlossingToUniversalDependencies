from translator.conversion.properties.auxiliary import split_feat_val
from translator.conversion.properties.layered_features import format_layered_feature
from unit import Unit

LAYERED_FEATURES = {'Person', 'Number'}
CLITIC_LAYER = 'obj'
VERB_LAYER = 'subj'

def format_verb_feats(verb: Unit) -> list[str]:
  verb_feats = verb.tag
  new_verb_feats = list[str]()
  for feat_val in verb_feats:
    feat, val = split_feat_val(feat_val)
    if feat in LAYERED_FEATURES:
      formatted = format_layered_feature(feat, VERB_LAYER, val)
      new_verb_feats.append(formatted)
    else:
      new_verb_feats.append(feat_val)
  return new_verb_feats

def get_formatted_clitic_agr_feats(clitic: Unit) -> list[str]:
  clitic_feats = clitic.tag
  clitic_agr_feats = list[str]()
  for feat_val in clitic_feats:
    feat, val = split_feat_val(feat_val)
    if feat in LAYERED_FEATURES:
      new_feat_val = format_layered_feature(feat, CLITIC_LAYER, val)
      clitic_agr_feats.append(new_feat_val)
    elif feat == 'Reflex':
      clitic_agr_feats.append(feat_val)
  return clitic_agr_feats
