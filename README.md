# Ebook word list generator for language learning #
# (PRE-ALPHA) #

This Python script generates lists of words per chapter with translation. Input is a folder of foreign language epubs, with subfolders for book series. Output is a pdf file per book, filtered for words already encountered in previous books and chapters.

The script parses words from epub text by chapter, using unicode categories to distinguish letters and non-seperator characters. This means it should work with any language that has enough word entries in apertium or en.wiktionary.org, and has words that:
- Start and end with a "letter".
- Don't contain "seperator" or "control" characters.
- Don't contain two non-"letters" in a row.

The script does not make any other assumptions about the language.

## Requirements and installation ##

Make sure you have Python 3.7+ and Pip installed.

Install ebooklib and beautifulsoup:
```pip install ebooklib beautifulsoup4```

You need LaTeX to generate the pdf, I use the apt package ```texlive-full```, and even though it is several GB's, I recommend you do the same.

Clone this repo:
```git clone git@github.com:evavh/ebook-wordlist.git```

Download an apertium language pair .dix file:
- Go [here](https://apertium.github.io/apertium-on-github/source-browser.html) (see [this page](https://wiki.apertium.org/wiki/List_of_language_pairs) for a clearer overview of available pairs)
- Click the pair you want (probably a *-eng pair)
- Download the .dix file from the github page.

Put this file in the cloned repo's root folder (where main.py is) and rename it to ```apertium.dix```

Download a wiktionary json file from [here](https://kaikki.org/dictionary/):
- Click the source language
- Click "All word senses" under "Word sense lists"
- Scroll down and click "Download JSON data for these senses"

Put this file in the cloned repo's root folder and rename it to ```wiktionary.json```.


## How to use ##

From the repo's root folder, run:
```python3 main.py <path to books>```
with the folder that contains your foreign language epubs.
Each folder inside the book root folder is treated as a series that must be read in order. All books and series are processed in alphabetical order, so you probably want to number them in the order you want to read them.

It will take a while to process the books, and then the pdf's will appear in the output folder inside the repo.
