#!/usr/bin/python3
import collections
import os
import argparse

import text_parsing
import file_io
import latex
import word_counting
import translating


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("root_folder", help="folder that contains books")
    return parser.parse_args()


if __name__ == '__main__':
    TIMES_UNTIL_KNOWN = 5
    WIKTIONARY_JSON = "wiktionary.json"
    APERTIUM_DIX = "apertium.dix"
    TEMP_FOLDER = "temp"
    OUTPUT_FOLDER = "output"

    root_folder = parse_arguments().root_folder
    book_paths = file_io.get_book_paths(root_folder)

    file_io.create_directory(OUTPUT_FOLDER)
    file_io.create_directory(TEMP_FOLDER)

    translations = translating.combine_dictionaries(APERTIUM_DIX,
                                                    WIKTIONARY_JSON)
    regex_strings = text_parsing.cache_regex_strings()

    seen_before = collections.defaultdict(int)

    if os.path.exists("already_known.txt"):
        with open("already_known.txt", 'r') as file:
            already_known_raw = file.read()
        already_known_words = text_parsing.get_words(already_known_raw,
                                                     regex_strings)
        for word in already_known_words:
            seen_before[word] = TIMES_UNTIL_KNOWN + 1

    for book_path in book_paths:
        book_title = os.path.basename(book_path)[:-5]

        book_tex_path = f"{TEMP_FOLDER}/{book_title}.tex"
        file_io.remove_file(book_tex_path)

        file_io.string_to_file(latex.LATEX_PRELUDE, book_tex_path)
        file_io.string_to_file("\\begin{center}\n{\\Huge \\textbf{Wordlist for"
                               " \"" + book_title+"\"}}\n\\end{center}\n\n"
                               + "\\setcounter{tocdepth}{2}\\tableofcontents"
                               + "\\renewcommand{\\baselinestretch}{0.5}",
                               book_tex_path)

        chapter_texts = file_io.get_chapter_texts(book_path)

        for index, chapter_text in enumerate(chapter_texts):
            print(f"Currently {len(seen_before)} words have been seen.")

            chapter_number = index + 1
            print((f"Processing chapter {chapter_number} of "
                   f"{len(chapter_texts)} of {book_title}..."))

            words = text_parsing.get_words(chapter_text.lower(), regex_strings)

            not_known, seen_before = word_counting.new_lists(words,
                                                             seen_before,
                                                             TIMES_UNTIL_KNOWN)

            print(f"Added {len(not_known)} words to chapter wordlist.\n")

            file_io.string_to_file("\\section{Chapter "+str(chapter_number)
                                   + " ("+str(len(not_known))+")}\n",
                                   book_tex_path)
            file_io.wordlist_to_file(not_known, book_tex_path, translations)

        file_io.string_to_file("\\end{document}", book_tex_path)
        file_io.latex_and_cleanup(TEMP_FOLDER, OUTPUT_FOLDER, book_tex_path)
