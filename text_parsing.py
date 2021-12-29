import re
import sys
import unicodedata


def get_words(text):
    word_pattern = r"(?:[a-z]+(?:[\-.][a-z]+)*[a-z])|[a-z]"
    words = re.findall(word_pattern, text)
    return words


def unicode_category_lists():
    result = {"letters": [], "non-separators": []}
    for i in range(sys.maxunicode):
        category = unicodedata.category(chr(i))

        if category.startswith('L'):
            result["letters"].append(chr(i))

        if not category.startswith('Z') and not category.startswith('C'):
            result["non-separators"].append(chr(i))

    return result


if __name__ == '__main__':
    norwegian_nonsense = ("jeg- jeg er. t-skjortene er ikke. jeg...og du. "
                          "han-som-ser er her. a leve.")
    unicode = unicode_category_lists()
    words = get_words(norwegian_nonsense)
    correct_words = ['jeg', 'jeg', 'er', 't-skjortene', 'er', 'ikke', 'jeg',
                     'og', 'du', 'han-som-ser', 'er', 'her', 'a', 'leve']
    assert (words == correct_words), f"words: {words} != {correct_words}"
