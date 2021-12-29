import re
import sys
import unicodedata


def get_words(text):
    unicode = unicode_category_lists()

    L = list_to_regex(unicode["letters"])
    NS = list_to_regex(unicode["non-separators"])

    word_pattern = f"(?:{L}+(?:{NS}{L}+)*{L})|{L}"
    words = re.findall(word_pattern, text)
    return words


def unicode_category_lists():
    result = {"letters": [], "non-separators": []}
    for i in range(sys.maxunicode):
        category = unicodedata.category(chr(i))

        if category.startswith('L'):
            result["letters"].append(chr(i))

        if not category.startswith('Z'):  # if not in a seperator category
            result["non-separators"].append(chr(i))

    return result


def list_to_regex(chars):
    TO_BE_ESCAPED = "]-^\\\""
    result = ""
    for char in chars:
        if char in TO_BE_ESCAPED:
            result += '\\'
        result += char

    result = "[" + result + "]"
    return result


if __name__ == '__main__':
    norwegian_nonsense = ("«Jeg- jeg er. T-skjortene er ikke. Jeg...óg du.»\n"
                          "Han-som-ser er her. «Å leve!»")

    words = get_words(norwegian_nonsense.lower())
    correct_words = ['jeg', 'jeg', 'er', 't-skjortene', 'er', 'ikke', 'jeg',
                     'óg', 'du', 'han-som-ser', 'er', 'her', 'å', 'leve']
    assert (words == correct_words), f"words: {words} != {correct_words}"
