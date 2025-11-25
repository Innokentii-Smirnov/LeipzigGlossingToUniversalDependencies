import os
from os import path
from tqdm.auto import tqdm
from .reading.text import read_sentences_from_file
from .conversion.text import convert_glossed_sentences_to_UD_sentences, conllu_to_file, conllu_to_json

SOURCE = 'Source unspecified'
URL = 'Webpage unspecified'
input_directory = 'input'
output_directory = 'output'
skipped_directory = 'skipped'

os.makedirs(output_directory, exist_ok=True)
os.makedirs(skipped_directory, exist_ok=True)

walk = list(os.walk(input_directory))
for dirpath, dirnames, filenames in tqdm(walk):
  relpath = path.relpath(dirpath, input_directory)
  for filename in filenames:
    shortname, ext = path.splitext(filename)
    if ext == '.txt':
      fullname = path.join(dirpath, filename)
      json_outfile = path.join(output_directory, shortname + '.json')
      conllu_outfile = path.join(output_directory, shortname + '_conllu.txt')
      skipped_outfile = path.join(skipped_directory, 'skipped_' + filename)
      text_sentences = read_sentences_from_file(fullname, skipped_outfile)
      ud_sentences = convert_glossed_sentences_to_UD_sentences(text_sentences)
      conllu_to_file(ud_sentences, conllu_outfile)
      conllu_to_json(ud_sentences, json_outfile, SOURCE, URL)
