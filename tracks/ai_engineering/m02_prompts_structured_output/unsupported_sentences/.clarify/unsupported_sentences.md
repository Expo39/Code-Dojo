# unsupported_sentences: clarifications

Pattern: support-check

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- A sentence ends at `.`, `!` or `?` followed by whitespace or the end; the mark stays in the returned sentence.
- Content words are lower-case letters and digits, minus the words in STOPWORDS; numbers count as words.
- The share is counted per sentence against each passage separately; the best single passage decides, never the combined words of several.
- A share exactly equal to `min_overlap` is supported.
- A sentence with no content words is treated as supported.
- No passages: every sentence with content words is unsupported; an empty answer returns an empty list.
- This is a cheap check, not a proof: it cannot tell a paraphrase from a lie (the discussion questions say what it misses).
