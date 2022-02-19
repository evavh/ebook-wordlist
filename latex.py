import os
import re

import file_io

LATEX_PRELUDE = ("\\documentclass[8pt]{article}\n"
                 "\\usepackage[utf8]{inputenc}\n"
                 "\\usepackage[T1]{fontenc}\n\\setcounter{secnumdepth}{0}\n"
                 "\\usepackage[a5paper,margin=1.5cm]{geometry}\n"
                 "\\usepackage[hidelinks]{hyperref}\n"
                 "\\parindent=1em\n\\usepackage{indentfirst}\n\n"
                 "\\begin{document}\n\n")


def escape_latex(string):
    translation_dict = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
                        "_": r"\_", "{": r"\{", "}": r"\}",
                        "~": r"\\textasciitilde", "^": r"\\textasciicircum",
                        "\\": r"\\textbackslash"}
    translation_table = str.maketrans(translation_dict)
    return string.translate(translation_table)


def remove_brackets(string):
    while '(' in string and ')' in string:
        string = re.sub(r" \([^()]*\)", "", string)
    return string


def deduplicate(list):
    result = []
    [result.append(x) for x in list if x not in result]
    return result


def to_latex_list(meanings):
    meanings = deduplicate(meanings)[:3]
    if "," in "".join(meanings) and len(meanings) > 1:
        result = ""
        for i, meaning in enumerate(meanings):
            result += f"{i+1}. {meaning} "
        result += "\n"
        return result
    else:
        return ", ".join(meanings)+"\n"


def expand_meanings(word, translations):
    result = []
    meanings = translations[word]
    for meaning in meanings:
        if meaning.form_of:
            root_word = meaning.content
            if root_word in translations:
                result.append("\\textbf{"+root_word+"}: " +
                              to_latex_list(expand_meanings(root_word,
                                                            translations)))
        else:
            result.append(remove_brackets(meaning.content))
    return result


def word_to_latex(word, translations):
    if word in translations:
        meanings = deduplicate(translations[word])
        formatted_word = to_latex_list(expand_meanings(word, translations))
        if len(meanings) == 1:
            meaning = meanings[0]
            if meaning.form_of and meaning.content in word:
                return formatted_word + "\n"
        return "\\textbf{"+word+"} - "+formatted_word+"\n"
    else:
        return ""


def latex_and_cleanup(temp_folder, output_folder, tex_path):
    # run pdflatex two times to make the table of contents work
    os.system(f"lualatex --output-directory={temp_folder} \"{tex_path}\"")
    os.system(f"lualatex --output-directory={temp_folder} \"{tex_path}\"")
    latex_file_root = tex_path[:-4]
    file_io.remove_file(latex_file_root+".aux")
    file_io.remove_file(latex_file_root+".log")
    file_io.remove_file(latex_file_root+".out")
    file_io.remove_file(latex_file_root+".toc")
    os.system(f"mv \"{latex_file_root}\".pdf {output_folder}")


if __name__ == '__main__':
    string = "This has brackets (remove this)"
    assert remove_brackets(string) == "This has brackets ",\
        f"Brackets still here?: {remove_brackets(string)}"
    string = "Nested brackets (very difficult (I think) this is)"
    assert remove_brackets(string) == "Nested brackets ",\
        f"Brackets still here?: {remove_brackets(string)}"
    string = "Brackets (everywhere) brackets (everywhere)"
    assert remove_brackets(string) == "Brackets  brackets ",\
        f"Brackets still here?: {remove_brackets(string)}"
