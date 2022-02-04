import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

import latex


def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def get_book_paths(root_folder):
    book_paths = []
    root_files = sorted(os.listdir(root_folder))
    for file in root_files:
        file_path = root_folder+'/'+file
        if os.path.isdir(file_path):
            series_path = file_path
            series_files = sorted(os.listdir(file_path))
            for file in series_files:
                file_path = series_path+'/'+file
                if file_path.endswith('.epub'):
                    book_paths.append(file_path)
        elif file_path.endswith('.epub'):
            book_paths.append(file_path)
    return book_paths


def get_chapter_texts(book_path):
    book = epub.read_epub(book_path)
    result = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            name = item.get_name().lower()
            content = item.get_content()
            if "chapter" in name or "part" in name:
                if "nextbook" not in name:
                    text = BeautifulSoup(content, features="lxml")\
                        .get_text(separator="\n")

                    result.append(text)
    return result


def format_meanings(meanings):
    if len(meanings) == 1:
        if isinstance(meanings[0], list):
            return meanings[0][0] + '\n'
        else:
            return meanings[0] + '\n'
    else:
        result = ""
        for index, meaning in enumerate(meanings):
            meaning = meaning[0]
            if isinstance(meaning, list):
                meaning = meaning[0]
            if index == 0:
                result += f"{index + 1}. {meaning}\n"
            else:
                result += f"\t\t\t\t\t{index + 1}. {meaning}\n"
        return result


def string_to_file(string, path):
    with open(path, 'a') as file:
        file.write(string)


def wordlist_to_file(frequency, path, translations):
    for word in frequency:
        word_latex = latex.word_to_latex(word, translations)
        string_to_file(word_latex, path)


if __name__ == '__main__':
    meanings = [['the act of guessing, sensing, suspecting; a clue, idea'],
                ['a very weak occurrence (of something)']]
    print(format_meanings(meanings))
    book_paths = get_book_paths("/home/eva/books")
    for book_path in book_paths:
        print(book_path)
