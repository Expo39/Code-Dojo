# parse_csv: clarifications

Pattern: line-parsing

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- The header is the first non-blank line.
- Strip spaces around values; values stay strings.
- Skip blank lines.
- Header only, or empty text: [].
- A row with the wrong number of fields: raise ValueError whose message contains the line number (1-based, counting every line of the text).
