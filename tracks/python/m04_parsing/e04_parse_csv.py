"""CSV text to a list of dicts (without the csv module).

Level: easy
Target: 20
Pattern: line-parsing

The first non-blank line is the header. Return one dict per data row, keys from
the header, values stripped of spaces. Skip blank lines. If a row has the wrong
number of fields, raise ValueError whose message contains the line number
(1-based, counting every line of the text).

    parse_csv("name, qty\napple, 3\npear,5")
    -> [{"name": "apple", "qty": "3"}, {"name": "pear", "qty": "5"}]
"""


def parse_csv(text):
    raise NotImplementedError
