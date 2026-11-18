"""Parse a simple config file.

Level: easy
Target: 15

Parse lines of the form `key = value` into a dict.

    parse_config("# db\nhost = localhost\nport=5432\n")
    -> {"host": "localhost", "port": 5432}

Trace by hand (work out the result yourself):

    parse_config("name = dojo\n# comment\nretries=3\n") -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify parse_config
"""


def parse_config(text):
    raise NotImplementedError
