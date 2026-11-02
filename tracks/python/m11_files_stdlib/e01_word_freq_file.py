"""Read a file, count words.

Level: easy
Target: 15
Pattern: files

Read the UTF-8 text file at `path` (a str or pathlib.Path). Return the n most
common words (lower case, strip .,!?;:"'() from both ends) as a list of
(word, count) tuples, most common first, ties alphabetical. A missing file
raises FileNotFoundError (let Python raise it).

Use `with open(path, encoding="utf-8") as f:` or pathlib.Path(path).read_text().
Then try collections.Counter.

Read: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
"""


def word_freq_file(path, n):
    raise NotImplementedError
