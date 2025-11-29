import os
from os import path
from tqdm.auto import tqdm
from translator.reading.text import read_sentences_from_file
from translator.conversion.text import convert_glossed_sentences_to_UD_sentences, conllu_to_file, conllu_to_json
from translator.model.glossing.sentence import log_filter
from logging import getLogger, FileHandler, Formatter

SOURCE = 'Source unspecified'
URL = 'Webpage unspecified'
input_directory = 'input'
output_directory = 'output'
skipped_directory = 'skipped'
log_directory = 'logs'

os.makedirs(output_directory, exist_ok=True)
os.makedirs(skipped_directory, exist_ok=True)
os.makedirs(log_directory, exist_ok=True)

logging_configuration = {
    'translator.model.glossing.word': (
      'gloss_issues',
      Formatter('%(sent_id)s\n%(message)s\n')
    ),
    'translator.conversion.properties.conversion': (
      'atr_val_issues',
      Formatter('%(sent_id)s\n%(segmentation)s\n%(gloss)s\n%(message)s\n')
    )
}

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

      # Set up logging for this text
      for logger_name, (issue_type, formatter) in logging_configuration.items():
        log_file_name = path.join(log_directory, f'{issue_type}_{shortname}.log')
        handler = FileHandler(log_file_name, 'w', encoding='utf-8')
        handler.addFilter(log_filter)
        logger = getLogger(logger_name)
        logger.addHandler(handler)
        handler.setFormatter(formatter)

      # Process the file
      text_sentences = read_sentences_from_file(fullname, skipped_outfile)
      ud_sentences = convert_glossed_sentences_to_UD_sentences(text_sentences)
      conllu_to_file(ud_sentences, conllu_outfile)
      conllu_to_json(ud_sentences, json_outfile, SOURCE, URL)

      # Stop logging for this text
      for logger_name, (issue_type, formatter) in logging_configuration.items():
        logger = getLogger(logger_name)
        for hdlr in logger.handlers:
          logger.removeHandler(hdlr)
