from os import path
import os
import json
from merging import merge_clitic_and_verb, format_verb_object

input_directory = 'output'
assert path.exists(input_directory)
output_directory = 'prefixed'
os.makedirs(output_directory, exist_ok=True)

for file_name in os.listdir(input_directory):
  short_name, ext = path.splitext(file_name)
  if ext == '.json':
    print(file_name)
    with open(path.join(input_directory, file_name), 'r', encoding='utf-8') as fin:
      text = json.load(fin)
      for sentence in text:
        tokens = sentence['tokens']
        i = 0
        while i < len(tokens):
          token = tokens[i]
          token_feats = token['tagsets'][0]
          if 'VERB' in token_feats:
            format_verb_object(token)
          elif i + 1 < len(tokens):
            next_token = tokens[i + 1]
            next_token_feats = next_token['tagsets'][0]
            if 'Clitic=Yes' in token_feats and 'VERB' in next_token_feats:
              del tokens[i]
              merge_clitic_and_verb(token, next_token)
          i += 1
    with open(path.join(output_directory, file_name), 'w', encoding='utf-8') as fout:
      json.dump(text, fout, ensure_ascii=False, indent=6)
