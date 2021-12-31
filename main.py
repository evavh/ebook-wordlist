#!/usr/bin/python3
import text_parsing
import file_io
import word_counting

if __name__ == '__main__':
    book_path = "book1.epub"
    chapter_texts = file_io.get_chapter_texts(book_path)

    for index, chapter_text in enumerate(chapter_texts):
        chapter_number = index + 1
        print((f"Processing chapter {chapter_number} of {len(chapter_texts)} "
               f"of {book_path[:-5]}..."))

        L, NS = text_parsing.cache_regex_strings()
        words = text_parsing.get_words(chapter_text.lower(), L, NS)

        freq_in_chapter = word_counting.frequency(words)
        print((f"There are {len(freq_in_chapter)} unique words in this "
              "chapter."))

        chapter_filename = f"{book_path[:-5]}chapter{chapter_number}.txt"
        file_io.wordlist_to_file(freq_in_chapter, chapter_filename)
