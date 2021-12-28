import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


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
                print(chapter)
                text = BeautifulSoup(content, features="lxml")\
                    .get_text(separator="\n")
                if previous_chapter is not None:
                    assert (chapter == previous_chapter + 1), \
                        (f"Previous chapter is {previous_chapter}, "
                         f"but this chapter is {chapter}")
                result.append(text)
                previous_chapter = chapter
    return result


if __name__ == '__main__':
    book_path = "book1.epub"
    chapter_texts = get_chapter_texts(book_path)
