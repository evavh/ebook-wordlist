#!/usr/bin/python3
import text_parsing
import file_io

if __name__ == '__main__':
    book_path = "book1.epub"
    chapter_texts = file_io.get_chapter_texts(book_path)

    for index, chapter_text in enumerate(chapter_texts):
        chapter_number = index + 1

        L, NS = text_parsing.cache_regex_strings()
        words = text_parsing.get_words(chapter_text.lower(), L, NS)

        if chapter_number == 1:
            print(words)
