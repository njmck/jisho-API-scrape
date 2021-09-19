# !/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @AUTHOR : njmck

import json
from urllib.request import urlopen
import ssl
import collections
import pandas as pd
import urllib



def jishoTagScrape(search_tags):
    '''
    Scrape all vocab using search tags.
    '''
    page_num = 1
    # These lists will populate with kanji, hiragana, and English definitions, and will
    # be printed as flashcards in a .txt file at the end.
    word_data_list = []
    # By doing <= 1000 (final_num), this will scrape 20,000 commonly-used Japanese words (20 words each page).
    # Any more than this will cause strange errors with duplicates. May be an API issue.
    last_page = False
    while last_page == False:
        print("Starting page " + str(page_num) + ".")
        # Go to jisho.org and look through words with desired tag.
        search_tag_str = '%20'.join([('%23' + i_0) for i_0 in search_tags])
        url = "http://jisho.org/api/v1/search/words?keyword=" + search_tag_str + "&page=" + str(page_num)
        page = urlopen(url, context=ssl._create_unverified_context())
        json_data = json.load(page)
        if page_num != 1:
            if all(i_0 in word_data for i_0 in json_data['data']):
                last_page = True
                return word_data_list
            else:
                word_data = json_data['data']
        else:
            word_data = json_data['data']
        word_data_list += word_data
        page_num += 1
    return word_data_list


def removeDuplicates(combined_list):
    '''
    Remove all duplicates in a list.
    '''
    no_of_dupes = 0
    unique_list = []
    for i_0 in combined_list:
        if i_0 not in unique_list:
            unique_list.append(i_0)
        else:
            no_of_dupes += 1
    print(str(no_of_dupes) + " duplicates removed from list.")
    return unique_list


def storeJSON(scraped_list, json_filename):
    '''
    Store the scraped vocabulary data as a json file.
    '''
    json_filename = str(json_filename)
    json_data = json.dumps(scraped_list)
    with open(json_filename, 'w') as jsonfile:
        json.dump(json_data, jsonfile)


def restoreJSON(json_filename):
    '''
    Restore previously-scraped data from a json file into an OrderedDict.
    '''
    with open(json_filename, 'r') as jsonfile:
        json_load = json.load(jsonfile)
    json_od = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(json_load)
    return json_od


def kanjiData(nested_lists):
    '''
    Creates a list of vocabulary which included the kanji.
    '''
    kanji_list = []
    for i_0 in nested_lists:
        kanji_child_list = []
        # Make kanji and empty string (i.e. don't include it) if
        # "Usually written using kana alone" is a tag.
        if "Usually written using kana alone" in i_0['senses'][0]['tags']:
            kanji_list.append(kanji_child_list)
        elif 'word' in i_0['japanese'][0]:
            for i_1 in i_0['japanese']:
                if 'word' in i_1:
                    kanji_child_list.append(i_1['word'])
            kanji_list.append(kanji_child_list)
        else:
            kanji_list.append(kanji_child_list)
    return kanji_list


def kanaData(nested_lists):
    '''
    Creates a list of vocabulary which includes kana only (no kanji).
    '''
    kana_list = []
    for i_0 in nested_lists:
        kana_child_list = []
        # Make kanji and empty string (i.e. don't include it) if
        # "Usually written using kana alone" is a tag.
        for i_1 in i_0['japanese']:
            if 'reading' in i_1:
                kana_child_list.append(i_1['reading'])
        kana_list.append(kana_child_list)
    return kana_list


def engData(nested_lists, pos_exclusion_list):
    '''
    Creates a list of English definitions.
    '''
    eng_list = []
    for i_0 in nested_lists:
        eng_child_list = []
        # Make kanji and empty string (i.e. don't include it) if
        # "Usually written using kana alone" is a tag.
        for i_1 in i_0['senses']:
            if 'english_definitions' in i_1:
                if 'parts_of_speech' not in pos_exclusion_list:
                    eng_child_list.append(i_1['english_definitions'])
        eng_list.append(eng_child_list)
    return eng_list


def readAndScrape(txt_filename):
    '''
    Scrape vocab of interest line-by-line instead of searching by tag in jishoTagScape.
    '''
    with open(txt_filename) as f:
        content = f.readlines()
    # List pre-processing and cleaning:
    content = [i_0.rstrip('\n') for i_0 in content]
    content = [(i_0.lstrip()).rstrip() for i_0 in content]
    content = [i_0 for i_0 in content if i_0 != ""]
    # These lists will populate with kanji, hiragana, and English definitions, and will
    # be printed as flashcards in a .txt file at the end.
    word_data_list = []
    # By doing <= 1000 (final_num), this will scrape 20,000 commonly-used Japanese words (20 words each page).
    # Any more than this will cause strange errors with duplicates. May be an API issue.
    for num_0, i_0 in enumerate(content):
        print("Starting word " + str(num_0 + 1) + " of " + str((len(content))))
        # Go to jisho.org and look through words with desired tag.
        url = "https://jisho.org/api/v1/search/words?keyword=" + urllib.parse.quote(i_0, encoding='utf-8') + "&page=" + str(1)
        page = urlopen(url, context=ssl._create_unverified_context())
        json_data = json.load(page)
        word_data = json_data['data']
        candidate_list = []
        # Disseminate the data for the queried word:
        for i_1 in word_data:
            entry_data = []
            for i_2 in i_1['japanese']:
                if 'word' in i_2:
                    entry_data.append(i_2['word'])
                if 'reading' in i_2:
                    entry_data.append(i_2['reading'])
            if i_0 in entry_data:
                candidate_list.append(i_1)
            # If more than one match, user can choose which one:
        if len(candidate_list) == 1:
            word_data_list.append(candidate_list[0])
        else:
            for num_1, i_3 in enumerate(candidate_list):
                print('----------[' + str(num_1 + 1) + ']----------')
                print(i_3)
            user_choice = int(input()) - 1
            # If user choice index is out of range, don't continue:
            if user_choice >= len(candidate_list) or not isinstance(user_choice, int):
                while user_choice >= len(candidate_list):
                    user_choice = int(input()) - 1
            # Append the user's choice:
            word_data_list.append(candidate_list[user_choice])
    return word_data_list


def partsOfSpeechData(nested_lists):
    '''
    Scrape English data.
    '''
    parts_of_speech_list = []
    for i_0 in nested_lists:
        parts_of_speech_child_list = []
        # Make kanji and empty string (i.e. don't include it) if
        # "Usually written using kana alone" is a tag.
        for i_1 in i_0['senses']:
            if 'parts_of_speech' in i_1:
                parts_of_speech_child_list.append(i_1['parts_of_speech'])
        parts_of_speech_list.append(parts_of_speech_child_list)
    return parts_of_speech_list


def tagsData(nested_lists):
    '''
    Scrape tags data.
    '''
    tags_list = []
    for i_0 in nested_lists:
        tags_child_list = []
        # Make kanji and empty string (i.e. don't include it) if
        # "Usually written using kana alone" is a tag.
        for i_1 in i_0['senses']:
            if 'tags' in i_1:
                tags_child_list.append(i_1['tags'])
        tags_list.append(tags_child_list)
    return tags_list


def kanjiFlashcardString(kanji_list, pos_exclusion_list, pos_list):
    '''
    Accepts a list of nested lists of kanji vocab.
    Returns a kanji string or an empty string depending if kanji is commonly used or not.
    '''
    kanji_str_list = []
    for i_0 in range(len(kanji_list)):
        for i_1 in pos_exclusion_list:
            if i_1 in pos_list[i_0][0]:
                kanji_str = ""
            elif kanji_list[i_0] == []:
                kanji_str = ""
            else:
                kanji_str = kanji_list[i_0][0]
        kanji_str_list.append(kanji_str)
    return kanji_str_list


def engFlashcardString(eng_list, pos_list, pos_exclusion_list, tags_list, tag_exclusion_list, newline):
    '''
    Accepts a list of nested lists of English definitions.
    Returns a string with the pos and definitions sorted.
    '''
    eng_str_list = []
    for i_0 in range(len(eng_list)):
        single_def_pos_list = [(newline + ', '.join(_) + ':' + newline) for _ in pos_list[i_0]]
        single_def_list = [('; '.join(_)) for _ in eng_list[i_0]]
        prev_pos = None
        def_num = 1
        eng_str_list_child = []
        for i_1 in range(len(single_def_pos_list)):
            include_def = True
            single_def_tag_list = tags_list[i_0][i_1]
            if single_def_tag_list == []:
                single_def_tag_str = ''
            else:
                single_def_tag_str = ' (' + ', '.join(single_def_tag_list) + ')'
            for i_2 in pos_exclusion_list:
                if i_2 in pos_list[i_0][i_1]:
                    include_def = False
            for i_2 in tag_exclusion_list:
                if i_2 in single_def_tag_list:
                    include_def = False
            if include_def:
                if single_def_pos_list[i_1] != prev_pos:
                    eng_str_list_child.append(single_def_pos_list[i_1])
                eng_str_list_child.append(str(def_num) + '. ' + single_def_list[i_1] + single_def_tag_str + newline)
                def_num += 1
                prev_pos = single_def_pos_list[i_1]
        eng_str_list_child_str = (''.join(eng_str_list_child))
        eng_str_list_child_str = eng_str_list_child_str[1:-1]
        eng_str_list.append(eng_str_list_child_str)
    return eng_str_list


def equalListLength(list_of_lists):
    '''
    Tests if lengths of lists are the same.
    '''
    it = iter(list_of_lists)
    the_len = len(next(it))
    if not all(len(l) == the_len for l in it):
        return False
    else:
        return True


def exportTSV(kanji_flashcard_str_list, kana_flashcard_str_list, eng_str_list, filename):
    """
    Print out Kanji + TAB + hiragana + TAB + English definition into a .txt file.
    Each word is on a separate line.
    """
    # Use the index_match to compile a dataframe:
    lists_to_df = [
        kanji_flashcard_str_list,
        kana_flashcard_str_list,
        eng_str_list,
    ]

    lists_to_df_col = ["Text 1", "Text 2", "Text 3"]

    if equalListLength(lists_to_df):
        flashcards_df = pd.DataFrame(lists_to_df).transpose()
        flashcards_df.columns = lists_to_df_col
    else:
        print('Dataframes not of equal length:')
        for i_0 in lists_to_df:
            print(len(i_0))

    flashcards_df.to_excel(filename, sheet_name='Sheet1', index=False)
