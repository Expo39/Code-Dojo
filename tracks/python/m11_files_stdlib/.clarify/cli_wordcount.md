# cli_wordcount: clarifications

Pattern: argparse-cli

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Words are separated by whitespace and stripped of . , ! ? ; : " ' ( ) at both ends;
  anything left empty after stripping is not a word.
- Without --ignore-case, "Up", "up" and "UP" are three different words; with it, all
  words are lower-cased before counting, and the report shows them lower-cased.
- Ties: alphabetical by the word as shown (Python's normal string order, so
  upper-case letters sort before lower-case).
- If --top is larger than the number of distinct words, list them all.
- An empty file gives just "words: 0\nunique: 0".
- --top must be a whole number of 1 or more; anything else ("abc", 0, -2) is a usage
  error: argparse prints a message and raises SystemExit. A missing `path` is a usage
  error too.
- A file that does not exist raises FileNotFoundError (let Python raise it).
- Importing the module must not parse arguments or print anything; run as a script,
  it prints the report.
