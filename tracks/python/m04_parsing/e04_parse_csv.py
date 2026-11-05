"""CSV text to a list of dicts (without the csv module).

Level: easy
Target: 20

Turn CSV text into a list of dicts, one per data row, with keys from the header
row. Do not use the csv module.

    parse_csv("name, qty\napple, 3\npear,5")
    -> [{"name": "apple", "qty": "3"}, {"name": "pear", "qty": "5"}]

Trace by hand (work out the result yourself):

    parse_csv("city, pop\nRome, 3\nOslo,1") -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify parse_csv
"""


def parse_csv(text):
    raise NotImplementedError
