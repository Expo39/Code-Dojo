# chunk_words: clarifications

Pattern: sliding-window

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Words are split on any whitespace; the chunks are joined with single spaces.
- `size` below 1, or `overlap` negative, or `overlap` not smaller than `size`: raise ValueError.
- An empty text, or one with only whitespace, gives an empty list.
- A text with fewer than `size` words gives one chunk.
- The last chunk may be shorter than `size`; there is never a last chunk made only of words already in the previous one.
- Return a new list; chunks are strings.
