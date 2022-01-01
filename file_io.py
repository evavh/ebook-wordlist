import os
import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def get_chapter_texts(book_path):
    book = epub.read_epub(book_path)
    result = []
    previous_chapter = None
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            name = item.get_name().lower()
            content = item.get_content()
            if "chapter" in name and "nextbook" not in name:
                chapter = re.search("chapter([0-9]{2})", name)[1]
                chapter = int(chapter)

                text = BeautifulSoup(content, features="lxml")\
                    .get_text(separator="\n")

                if previous_chapter is not None:
                    assert (chapter == previous_chapter + 1), \
                        (f"Previous chapter is {previous_chapter}, "
                         f"but this chapter is {chapter}")

                result.append(text)
                previous_chapter = chapter
    return result


def string_to_file(string, path):
    with open(path, 'a') as file:
        file.write(string)


def wordlist_to_file(frequency, path):
    sorted_words = sorted(frequency.keys(),
                          key=frequency.get, reverse=True)
    with open(path, 'a') as file:
        for word in sorted_words:
            file.write(f"{frequency[word]}\t{word}\n")
