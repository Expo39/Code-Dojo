# same_serial: clarifications

Pattern: string-cleaning

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Digits count: "A1" and "A7" differ.
- Order matters: "AB-12" and "AB-21" are different serials.
- One extra letter or digit makes them different.
- Both empty, or both only punctuation and spaces: True.
