import json
import xml.etree.ElementTree as ET
import collections


def parse_apertium(filename):
    xml_tree = ET.parse(filename)
    root = xml_tree.getroot()
    result = collections.defaultdict(list)

    for child in root:
        if child.tag == "section":
            section = child

    for child in section:
        if child.tag == "e":
            if child[0].tag == "p":
                item = child[0]
                word = item[0].text
                translation = item[1].text
                result[word].append(translation)
    return result


def parse_wiktionary(filename):
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


def combine_dictionaries(apertium_filename, wiktionary_filename):
    result = parse_apertium(apertium_filename)
    wiktionary = parse_wiktionary(wiktionary_filename)

    for word in wiktionary:
        if word not in result:
            result[word] = wiktionary[word]

    return result


if __name__ == '__main__':
    apertium = parse_apertium("apertium.dix")
    wiktionary = parse_wiktionary("wiktionary.json")
    print(f"Found {len(apertium.keys())} unique words in apertium file")
    print(f"Found {len(wiktionary.keys())} unique words in wiktionary file")

    translations = combine_dictionaries("apertium.dix", "wiktionary.json")
    print(f"Combined they have {len(translations.keys())} unique words")
