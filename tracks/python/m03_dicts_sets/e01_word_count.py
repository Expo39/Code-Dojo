"""Count words.

Level: easy
Target: 10
Pattern: counting

Return a dict mapping each word (lower case) to how often it appears.
Words are separated by whitespace; strip the punctuation .,!? from both ends.

    word_count("The cat and the hat.") -> {"the": 2, "cat": 1, "and": 1, "hat": 1}
    word_count("") -> {}

Write it with a plain dict and .get() first; then try collections.Counter.
"""


def word_count(text):
    raise NotImplementedError
