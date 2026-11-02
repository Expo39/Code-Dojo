# parse_pairs: clarifications

Pattern: parse-then-act

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Keys can be anything: do not assume which keys exist ("colour red size XL").
- Values stay strings.
- Blank lines are skipped; extra spaces are ignored.
- Empty text: [].
- A line with an odd number of tokens: raise ValueError.
