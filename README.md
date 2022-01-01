# Ebook word list generator for language learning #
# (WORK IN PROGRESS) #
This Python script will generate lists of words per chapter with translation. Input will be a folder of foreign language epubs, output will be sorted by frequency and filtered for words already encountered in previous books and chapters.

The script parses words from epub text by chapter, using unicode categories to distinguish letters and non-seperator characters. This means it could work with any language, assuming that a word starts and ends with a "letter", doesn't have a "seperator" or "control character" in it, and that a word does not contain two non-"letters" in a row.

Currently the input is a file in the projects' root directory called "book1.epub", and the output is a .txt file per chapter. This file contains the words that are new in that chapter, and the words that have been seen before, but less than 15 times, all sorted by how often they occur in the chapter.
