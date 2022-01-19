import os
import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

LATEX_PRELUDE = ("\\documentclass[8pt]{article}\n"
                 "\\usepackage[utf8]{inputenc}\n"
                 "\\usepackage[T1]{fontenc}\n\\setcounter{secnumdepth}{0}\n"
                 "\\usepackage[a5paper,margin=1.5cm]{geometry}\n"
                 "\\usepackage[hidelinks]{hyperref}\n"
                 "\\parindent=1em\n\\usepackage{indentfirst}\n\n"
                 "\\begin{document}\n\n")


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
                    assert (chapter == previous_chapter + 1),\
                        (f"Previous chapter is {previous_chapter}, "
                         f"but this chapter is {chapter}")

                result.append(text)
                previous_chapter = chapter
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


def escape_latex(string):
    translation_dict = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
                        "_": r"\_", "{": r"\{", "}": r"\}",
                        "~": r"\\textasciitilde", "^": r"\\textasciicircum",
                        "\\": r"\\textbackslash"}
    translation_table = str.maketrans(translation_dict)
    return string.translate(translation_table)


def unpack_list(meaning):
    if isinstance(meaning, list):
        return meaning[0]


def word_to_latex(word, translations):
    if word in translations:
        result = "\n\\subsubsection{"+word+"}"

        meanings = translations[word]
        if len(meanings) == 1:
            result += "\n"+escape_latex(unpack_list(meanings[0])) + "\n"
        else:
            result += "\n\\begin{enumerate}\n"
            for meaning in meanings[:3]:
                result += "\\item "+escape_latex(unpack_list(meaning)) + "\n"
            result += "\\end{enumerate}\n"

        return result
    else:
        return ""


def string_to_file(string, path):
    with open(path, 'a') as file:
        file.write(string)


def wordlist_to_file(frequency, path, translations):
    for word in frequency:
        word_latex = word_to_latex(word, translations)
        string_to_file(word_latex, path)


def latex_and_cleanup(temp_folder, output_folder, tex_path):
    # run pdflatex to times to make the table of contents work
    os.system(f"lualatex --output-directory={temp_folder} \"{tex_path}\"")
    os.system(f"lualatex --output-directory={temp_folder} \"{tex_path}\"")
    latex_file_root = tex_path[:-4]
    remove_file(latex_file_root+".aux")
    remove_file(latex_file_root+".log")
    remove_file(latex_file_root+".out")
    remove_file(latex_file_root+".toc")
    os.system(f"mv \"{latex_file_root}\".pdf {output_folder}")


if __name__ == '__main__':
    meanings = [['the act of guessing, sensing, suspecting; a clue, idea'],
                ['a very weak occurrence (of something)']]
    print(format_meanings(meanings))
    book_paths = get_book_paths("/home/eva/books")
    for book_path in book_paths:
        print(book_path)
