# !/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @AUTHOR : njmck

import jisho_API_functions as jishoAPI
import os.path


# Method 1: Scrape data based on a tag:
search_tags = ['jlpt-n1']
nested_lists = jishoAPI.jishoTagScrape(search_tags)

# Method 2: Alternatively, read a .txt file and scrape a json of contained words:
txt_filename = "word_list.txt"
read_file = readAndScrape(txt_filename)

# Check for duplicates:
remove_dupes = jishoAPI.removeDuplicates(nested_lists)
nested_lists = remove_dupes

# Make a directory for json files:
json_files_dir = 'json_files'
if os.path.isdir(json_files_dir):
	print("Directory for json files exists.")
else:
	os.mkdir(json_files_dir)
	print("Directory for json files does not exist. Making json file directory.")

# Store data as json data:
json_files_dir = 'json_files'
json_filename = json_files_dir + '/' + '_'.join(search_tags) + '.json'
jishoAPI.storeJSON(nested_lists, json_filename)

# Load the stored json file:
json_filename = "nested_lists.json"
list_restore = jishoAPI.restoreJSON(json_filename)
nested_lists = list_restore

# kanji list:
kanji_list = jishoAPI.kanjiData(nested_lists)

# kana list:
kana_list = jishoAPI.kanaData(nested_lists)

# English list:
pos_exclusion_list = ['Place', 'Wikipedia definition']
eng_list = jishoAPI.engData(nested_lists, pos_exclusion_list)

# Parts of speech list:
pos_list = jishoAPI.partsOfSpeechData(nested_lists)

# Tags list:
tags_list = jishoAPI.tagsData(nested_lists)

# Make strings for each line of :
tag_exclusion_list = ['Archaism'] # Exclude the whole definition
tags_not_written = ['Usually written using kana alone'] # Just don't write it down

kanji_flashcard_str_list = jishoAPI.kanjiFlashcardString(kanji_list, pos_exclusion_list, pos_list)

# kana strings:
kana_flashcard_str_list = [i_0[0] for i_0 in kana_list]

# English flashcard strings:
eng_flashcard_str_list = jishoAPI.engFlashcardString(eng_list, pos_list, pos_exclusion_list, tags_list, tag_exclusion_list, "|")

# Print in a flashcard friendly .txt file:
filename = 'output_files/' + '-'.join(search_tags) + '_flashcards.xlsx'
jishoAPI.exportTSV(kanji_flashcard_str_list, kana_flashcard_str_list, eng_flashcard_str_list, filename)
