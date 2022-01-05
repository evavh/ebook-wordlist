import json
import collections


def parse_dictionary(filename):
    result = collections.defaultdict(list)

    with open(filename, 'r', encoding="utf-8") as file:
        for line in file:
            entry = json.loads(line)
            word = entry["word"].lower()
            meanings = entry["senses"]
            for meaning in meanings:
                if "raw_glosses" in meaning:
                    result[word].append(meaning["raw_glosses"])

    return result


if __name__ == '__main__':
    translations = parse_dictionary("dictionary.json")
    print(translations)
