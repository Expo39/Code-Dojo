# parse_config: clarifications

Pattern: line-parsing

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Ignore blank lines and lines starting with #.
- Strip spaces around keys and values.
- Values made only of digits become int; everything else stays a string.
- A repeated key: the last one wins.
- A value may contain "=" itself: "query = a=b" -> "a=b".
- Any other line without "=": raise ValueError.
