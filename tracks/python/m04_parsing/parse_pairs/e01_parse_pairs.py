"""Records from "key value key value" lines.

Level: easy
Target: 15

(A real live-coding interview question.)

Each line of `text` holds one record as alternating keys and values separated by
spaces. Return a list of dicts, one per line.

    parse_pairs("name Alice age 30\nname Bob city Rome")
    -> [{"name": "Alice", "age": "30"}, {"name": "Bob", "city": "Rome"}]

Trace by hand (work out the result yourself):

    parse_pairs("colour red size L\nsize M") -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify parse_pairs
"""


def parse_pairs(text):
    raise NotImplementedError
