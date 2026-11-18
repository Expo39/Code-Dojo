# parse_duration: clarifications

Pattern: char-scanning

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Units are h, m and s, each at most once, in that order: "1h2m3s" -> 3723.
- Anything else raises ValueError: "", "10" (no unit), "5x", "m5", "1m1h", "1h1h".
