"""Run-length encoding.

Level: easy
Target: 15
Pattern: runs

Replace each run of the same character by the character and the run length.

    compress("aaabcc") -> "a3b1c2"
    compress("abca") -> "a1b1c1a1"
    compress("") -> ""

Think: what do you do with the last run when the loop ends?
"""


def compress(text):
    raise NotImplementedError
