#!/usr/bin/python3
import collections


def frequency(words):
    result = collections.defaultdict(int)

    for word in words:
        result[word] += 1

    return result


def add_frequencies(freq1, freq2):
    result = collections.defaultdict(int)

    for word in freq1:
        result[word] += freq1[word]
    for word in freq2:
        result[word] += freq2[word]

    return result


def freq_of_unseen(freq, frequency_of_seen):
    result = {}

    for word in freq:
        if word not in frequency_of_seen:
            result[word] = freq[word]

    return result


def get_freq_of_repeated(freq, freq_of_unseen, known_words):
    result = {}

    for word in freq:
        if word not in freq_of_unseen and word not in known_words:
            result[word] = freq[word]

    return result


if __name__ == '__main__':
    words = ["here", "are", "some", "words", "these", "words", "are", "great",
             "words"]
    correct_frequency = {"here": 1, "are": 2, "some": 1, "words": 3,
                         "these": 1, "great": 1}
    assert frequency(words) == correct_frequency,\
        f"generated {frequency(words)}, correct is {correct_frequency}"

    freq1 = collections.defaultdict(int)
    freq2 = collections.defaultdict(int)
    freq1["test"] = 2
    freq2["test"] = 2
    freq2["notthere"] = 3

    correct_add = collections.defaultdict(int)
    correct_add["test"] = 4
    correct_add["notthere"] = 3
    assert (add_frequencies(freq1, freq2) == correct_add), \
        ("freq1 + freq2={correct_add}, "
         f"add_frequencies  yields {add_frequencies(freq1,freq2)}")
