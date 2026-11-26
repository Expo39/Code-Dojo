"""Flag the sentences of an answer that no source supports.

Level: medium
Target: 25

A model told to answer from supplied passages still sometimes adds claims that are in none of
them. A cheap first check compares the words. Write `unsupported_sentences(answer, passages,
min_overlap)`:

- Split `answer` into sentences: a sentence ends at `.`, `!` or `?` followed by whitespace or
  the end of the text; keep the ending mark and strip surrounding whitespace.
- The content words of a text are its lower-case words made of letters and digits
  (`re.findall("[a-z0-9]+", text.lower())`) without the words in `STOPWORDS`.
- A sentence is supported when, for at least one single passage, the share of its content
  words that also appear among that passage's content words is at least `min_overlap`.
  A sentence with no content words is supported.
- Return the unsupported sentences, in order.

    passages = ["Refunds are issued within 5 days of the return."]
    unsupported_sentences("Refunds are issued within 5 days. We also offer free shipping worldwide.",
                          passages, 0.6)
    -> ["We also offer free shipping worldwide."]

Trace by hand (the list returned):

    passages = ["Paris is the capital of France."]
    unsupported_sentences("Paris is the capital of France. It has 2 million people!", passages, 0.5) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify unsupported_sentences
"""

import re

STOPWORDS = {"a", "an", "the", "we", "are", "is", "of", "to", "in", "and", "or", "it", "this", "that",
             "for", "on", "with", "as", "be"}


def unsupported_sentences(answer, passages, min_overlap):
    raise NotImplementedError
