#!/usr/bin/python3
import collections

import text_parsing
import file_io
import word_counting
import translating

if __name__ == '__main__':
    TIMES_UNTIL_KNOWN = 15
    WIKTIONARY_JSON = "dictionary.json"
    OUTPUT_FOLDER = "output"
    book_path = "book1.epub"
    book_title = book_path[:-5]

    file_io.create_directory(OUTPUT_FOLDER)
    book_tex_path = f"{OUTPUT_FOLDER}/{book_title}.tex"
    file_io.remove_file(book_tex_path)

    file_io.string_to_file(file_io.LATEX_PRELUDE, book_tex_path)
    file_io.string_to_file("\\begin{center}\n{\\Huge \\textbf{Wordlist for "
                           + book_title+"}}\n\\end{center}\n\n"
                           + "\\setcounter{tocdepth}{2}\\tableofcontents",
                           book_tex_path)

    translations = translating.parse_dictionary(WIKTIONARY_JSON)
    L, NS = text_parsing.cache_regex_strings()

    chapter_texts = file_io.get_chapter_texts(book_path)

    freq_of_seen = collections.defaultdict(int)

    for index, chapter_text in enumerate(chapter_texts):
        known_words = word_counting.known_words(freq_of_seen,
                                                TIMES_UNTIL_KNOWN)
        print((f"Currently {len(freq_of_seen)} words have been seen, of which "
               f"{len(known_words)} are fully known.\n"))

        chapter_number = index + 1
        print((f"Processing chapter {chapter_number} of {len(chapter_texts)} "
               f"of {book_path[:-5]}..."))

        words = text_parsing.get_words(chapter_text.lower(), L, NS)

        freq_in_chapter = word_counting.frequency(words)

        freq_of_unseen = word_counting.freq_of_unseen(freq_in_chapter,
                                                      freq_of_seen)
        freq_of_repeated = word_counting.freq_of_repeated(freq_in_chapter,
                                                          freq_of_unseen,
                                                          known_words)

        freq_of_seen = word_counting.add_frequencies(freq_of_seen,
                                                     freq_in_chapter)

        print((f"There are {len(freq_in_chapter)} unique words in this "
              f"chapter,\nof which {len(freq_of_unseen)} are yet unseen,"
               f"\nof which {len(freq_of_repeated)} words have been "
               "seen before but are not yet fully known."))

        file_io.string_to_file("\\section{Chapter "+str(chapter_number)+"}\n",
                               book_tex_path)
        file_io.string_to_file("\\subsection{New words}\n", book_tex_path)
        file_io.wordlist_to_file(freq_of_unseen, book_tex_path, translations)

        file_io.string_to_file("\\subsection{Repeated words}\n",
                               book_tex_path)
        file_io.wordlist_to_file(freq_of_repeated, book_tex_path, translations)

    file_io.string_to_file("\\end{document}", book_tex_path)

    known_words = word_counting.known_words(freq_of_seen,
                                            TIMES_UNTIL_KNOWN)
    with open("known_words.txt", 'w') as file:
        file.writelines(known_words)
