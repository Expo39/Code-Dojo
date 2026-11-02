# top_endpoints: clarifications

Pattern: parse-count-sort

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Count only successful requests: status 200 to 299.
- Ties: by path, alphabetically.
- Skip malformed lines: not exactly 4 fields, or a status that is not a number.
- n larger than the number of paths: all of them.
- No lines: [].
