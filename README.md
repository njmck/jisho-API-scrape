# jisho-API-scrape
## Useful Python functions for scraping data from the popular online Japanese-English dictionary website jisho.org

### jisho_API_main.py:
Contains the main script that utilises functions from jisho_API_functions.
You can specify search tags to scrape all words of a particular type, or you can scrape only a list of words you're interested in using a separate .txt file with each word separated on a new line.
After running the whole script, Japanese kanji, kana, and English definition information can be exported to an Excel spreadsheet using Pandas, which is compatible with [Flashcards Deluxe](https://orangeorapple.com/Flashcards/), a flashcard study app for smarthphones.

### jisho_API_functions.py:
Contains all the functions used in the main script. This file must therefore be imported when using the main script.

### 'output_files' directory:
Used for dumping output files such as spreadsheets containing vocabulary.

### 'json_files' directory:
Used for storing json files which contain vocabulary information scraped from jisho.org. json files can be stored here after scraping jisho.org using the main script, and also stored here to save time scraping in the future.