"""Records from "key value key value" lines.

Level: easy
Target: 15
Pattern: parse-then-act

(A real live-coding interview question.)

Each non-blank line holds one record as alternating keys and values separated
by spaces. Return a list of dicts, one per line. Read the keys FROM THE DATA:
do not assume which keys exist. Raise ValueError if a line has an odd number of
tokens.

    parse_pairs("name Alice age 30\nname Bob city Rome")
    -> [{"name": "Alice", "age": "30"}, {"name": "Bob", "city": "Rome"}]

Edge cases: empty text, blank lines, extra spaces, odd token count.
"""


def parse_pairs(text):
    raise NotImplementedError
