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


def unpack_list(meaning):
    if isinstance(meaning, list):
        return meaning[0]
    else:
        return meaning


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
