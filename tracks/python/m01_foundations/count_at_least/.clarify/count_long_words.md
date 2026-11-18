# count_long_words: clarifications

Pattern: accumulator

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Empty list: 0.
- A word exactly `min_length` characters long counts.
- No word long enough: 0.
- `min_length` can be 0: then every word counts, including the empty string.
- Words contain letters only; count every character.
