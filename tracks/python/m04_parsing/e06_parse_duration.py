"""Duration strings to seconds.

Level: medium
Target: 20
Pattern: char-scanning

Convert strings like "1h30m", "45m", "2h", "90s", "1h2m3s" to a number of
seconds. Units are h, m, s, each at most once, in that order. Raise ValueError
for anything else ("", "10", "5x", "m5", "1m1h").

    parse_duration("1h30m") -> 5400
    parse_duration("90s") -> 90
"""


def parse_duration(text):
    raise NotImplementedError
