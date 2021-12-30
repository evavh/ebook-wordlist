#!/usr/bin/python3
import collections


def frequency(words):
    result = collections.defaultdict(int)

    for word in words:
        result[word] += 1

    return result


if __name__ == '__main__':
    words = ["here", "are", "some", "words", "these", "words", "are", "great",
             "words"]
    correct_frequency = {"here": 1, "are": 2, "some": 1, "words": 3,
                         "these": 1, "great": 1}
    print(frequency(words))
    assert frequency(words) == correct_frequency,\
        f"generated {frequency(words)}, correct is {correct_frequency}"
