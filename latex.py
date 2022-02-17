import os

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


def to_latex_list(meanings):
    if "," in "".join(meanings) and len(meanings) > 1:
        result = "\n\\begin{enumerate}\n"
        for meaning in meanings:
            result += "\\item " + meaning
        result += "\\end{enumerate}\n"
        return result
    else:
        return "- "+", ".join(meanings)+"\n"


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
            result.append(meaning.content)
    return result


def word_to_latex(word, translations):
    if word in translations:
        formatted_word = to_latex_list(expand_meanings(word, translations))
        return "\\textbf{"+word+"} "+formatted_word+"\n"
    else:
        return ""


def latex_and_cleanup(temp_folder, output_folder, tex_path):
    # run pdflatex to times to make the table of contents work
    os.system(f"lualatex --output-directory={temp_folder} \"{tex_path}\"")
    os.system(f"lualatex --output-directory={temp_folder} \"{tex_path}\"")
    latex_file_root = tex_path[:-4]
    file_io.remove_file(latex_file_root+".aux")
    file_io.remove_file(latex_file_root+".log")
    file_io.remove_file(latex_file_root+".out")
    file_io.remove_file(latex_file_root+".toc")
    os.system(f"mv \"{latex_file_root}\".pdf {output_folder}")
