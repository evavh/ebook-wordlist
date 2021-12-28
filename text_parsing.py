import re


def get_words(text):
    word_pattern = r"(?:[a-z]+(?:[\-.][a-z]+)*[a-z])|[a-z]"
    words = re.findall(word_pattern, text)
    return words


if __name__ == '__main__':
    norwegian_nonsense = ("jeg- jeg er. t-skjortene er ikke. jeg...og du. "
                          "han-som-ser er her. a leve.")
    words = get_words(norwegian_nonsense)
