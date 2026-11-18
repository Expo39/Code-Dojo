# find_dates: clarifications

Pattern: regex-groups

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Exactly four digits, dash, two digits, dash, two digits: "2024-1-5" is not a date.
- Month must be 01 to 12 and day 01 to 31; anything else (2024-13-01, 2024-05-00) is skipped.
- No calendar check beyond that: 2024-02-31 counts.
- A date glued to more digits is part of a longer number and does not count ("12024-01-05", "2024-01-055").
- A date next to punctuation or brackets counts, e.g. "(2025-02-28)," or "2025-03-07."
- Values are ints, so 2024-03-05 gives (2024, 3, 5).
- Duplicates are kept, in order of appearance.
- No dates, or empty text: [].
