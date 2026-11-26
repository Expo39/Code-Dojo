"""Cut a long text into overlapping chunks.

Level: medium
Target: 20

Before a document can be searched it is cut into chunks. Chunks that overlap a little keep a
sentence that falls on a boundary whole in at least one chunk. Write `chunk_words(text, size,
overlap)`:

- Split `text` into words on whitespace. A chunk holds at most `size` words, joined with
  single spaces.
- Each chunk starts `size - overlap` words after the start of the previous one, so
  neighbouring chunks share `overlap` words.
- The chunks must cover every word, and the last chunk stops at the end of the text: do not
  add a final chunk that is only repeated words.
- Return the list of chunks.

    chunk_words("a b c d e f g", 4, 1) -> ["a b c d", "d e f g"]

Trace by hand (work out every chunk):

    chunk_words("one two three four five six seven eight nine", 4, 2) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify chunk_words
"""


def chunk_words(text, size, overlap):
    raise NotImplementedError
