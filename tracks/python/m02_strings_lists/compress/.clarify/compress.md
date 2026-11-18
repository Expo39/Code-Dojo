# compress: clarifications

Pattern: runs

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Empty string: "".
- A character can appear in several runs: "abca" -> "a1b1c1a1".
- Long runs use the full number: 12 z's -> "z12".
