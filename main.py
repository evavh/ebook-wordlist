import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

book = epub.read_epub("book1.epub")
for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        name = item.get_name().lower()
        content = item.get_content()
        if "chapter" in name and "nextbook" not in name:
            chapter = re.search("chapter([0-9]{2})", name)[1]
            chapter = int(chapter)
            text = BeautifulSoup(content).get_text()
