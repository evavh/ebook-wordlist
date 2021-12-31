#!/usr/bin/python3
import collections

import text_parsing
import file_io
import word_counting

if __name__ == '__main__':
    TIMES_UNTIL_KNOWN = 15
    book_path = "book1.epub"

    chapter_texts = file_io.get_chapter_texts(book_path)

    freq_of_seen = collections.defaultdict(int)

    for index, chapter_text in enumerate(chapter_texts):
        known_words = [word for word in freq_of_seen
                       if freq_of_seen[word] >= TIMES_UNTIL_KNOWN]
        print((f"Currently {len(freq_of_seen)} words have been seen, of which "
               f"{len(known_words)} are fully known.\n"))

        chapter_number = index + 1
        print((f"Processing chapter {chapter_number} of {len(chapter_texts)} "
               f"of {book_path[:-5]}..."))

        L, NS = text_parsing.cache_regex_strings()
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
              f"chapter,\nof which {len(freq_of_unseen)} are previously unseen,"
               f"\nof which {len(freq_of_repeated)} words have been "
               "seen before but are not yet fully known."))

        chapter_filename = f"{book_path[:-5]}chapter{chapter_number}.txt"

        file_io.wordlist_to_file(freq_in_chapter, chapter_filename)
