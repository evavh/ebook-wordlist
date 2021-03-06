import re
import sys
import unicodedata


def unicode_category_lists():
    result = {"letters": [], "non-separators": []}
    for i in range(sys.maxunicode):
        category = unicodedata.category(chr(i))

        if category.startswith('L'):
            result["letters"].append(chr(i))

        # Z means seperator, C means control character (\n is one of them)
        if not category.startswith('Z') and not category.startswith('C'):
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


def cache_regex_strings():
    unicode = unicode_category_lists()

    L = list_to_regex(unicode["letters"])
    NS = list_to_regex(unicode["non-separators"])

    return (L, NS)


def get_words(text, regex_strings):
    L, NS = regex_strings
    word_pattern = f"(?:{L}+(?:{NS}{L}+)*{L})|{L}"
    words = re.findall(word_pattern, text)
    return words


if __name__ == '__main__':
    norwegian_nonsense = ("H\nerr Kapitel er vanskelig. «Jeg- jeg er. "
                          "T-skjortene er ikke. Jeg...óg du.»\n"
                          "Han-som-ser er her. «Å leve!»")
    L, NS = cache_regex_strings()
    words = get_words(norwegian_nonsense.lower(), L, NS)
    correct_words = ['h', 'err', 'kapitel', 'er', 'vanskelig', 'jeg', 'jeg',
                     'er', 't-skjortene', 'er', 'ikke', 'jeg', 'óg', 'du',
                     'han-som-ser', 'er', 'her', 'å', 'leve']
    assert (words == correct_words), f"words: {words} != {correct_words}"
