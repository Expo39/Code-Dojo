"""Parse a simple config file.

Level: easy
Target: 15
Pattern: line-parsing

Lines look like `key = value`. Ignore blank lines and lines starting with #.
Strip spaces around keys and values. Convert values made only of digits to int.
If a key repeats, the last one wins. Raise ValueError for a line without "=".

    parse_config("# db\nhost = localhost\nport=5432\n")
    -> {"host": "localhost", "port": 5432}

Note: a value may itself contain "=" (e.g. `query = a=b`); split only on the first one.
"""


def parse_config(text):
    raise NotImplementedError
