# sensor_summary: clarifications

Pattern: parse-group-aggregate

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- avg is rounded to 2 decimals; min, max and avg are floats.
- Skip blank lines, lines without exactly 3 fields, and lines whose value is not a number.
- Empty text: {}.
