from os import path
import os
import json
from word import Token
from constituent import Constituent
from processing import process_elements

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
        process_elements(sentence['tokens'], Token)
        process_elements(sentence['constituents'], Constituent)
        sentence['length'] = len(sentence['tokens'])
    with open(path.join(output_directory, file_name), 'w', encoding='utf-8') as fout:
      json.dump(text, fout, ensure_ascii=False, indent=6)
