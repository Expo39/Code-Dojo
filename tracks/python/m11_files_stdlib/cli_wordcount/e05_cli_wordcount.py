"""A word-count command-line tool.

Level: medium
Target: 25

Write a small command-line tool in this file. main(argv) takes the arguments as a
list of strings (like sys.argv[1:]), parses them with argparse and returns the
report as a str:

- `path`: the UTF-8 text file to read (required)
- `--top N`: how many words to list (default 3)
- `--ignore-case`: treat "The" and "the" as the same word (lower-case them)

The report is lines joined by "\n" (no trailing newline): "words: <total>", then
"unique: <distinct words>", then one "<word> <count>" line per top word, most
common first. Running the file as a script (python e05_cli_wordcount.py notes.txt)
prints main(sys.argv[1:]); importing it must not run anything.

    notes.txt contains "the cat saw the dog the end"
    main(["notes.txt", "--top", "2"]) -> "words: 7\nunique: 5\nthe 3\ncat 1"

Trace by hand (work out the result yourself):

    log.txt contains "Up up down Up left up"
    main(["log.txt", "--ignore-case", "--top", "2"]) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify cli_wordcount

Read: https://docs.python.org/3/library/argparse.html (the tutorial is linked at the top)
"""


def main(argv):
    raise NotImplementedError
