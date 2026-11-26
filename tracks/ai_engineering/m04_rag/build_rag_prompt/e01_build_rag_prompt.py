"""Build a prompt for a retrieval-augmented answer, within a budget.

Level: medium
Target: 25

A RAG system has retrieved passages with a relevance score and must fit the best ones into a
prompt of limited size. Write `build_rag_prompt(question, passages, max_words)`:

- `passages` is a list of dicts with `id`, `text` and `score`.
- Take passages from the highest score to the lowest (equal scores keep their input order).
  Add a passage if the words in all chosen passage texts stay within `max_words`; if it does
  not fit, skip it and try the next one.
- Return `(prompt, used_ids)`: the prompt and the ids of the chosen passages, in prompt order.
- The prompt has these parts joined by a blank line (`"\n\n"`):
  1. `Answer using only the passages below. Cite passage ids in square brackets, like [p1]. If the passages do not contain the answer, say: not in the documents.`
  2. the passages, one per line as `[id] text` (omitted when none was chosen)
  3. `Question: <question>` then a newline and `Answer:`

    build_rag_prompt("When is it open?", [{"id": "p1", "text": "Open 9 to 5.", "score": 0.9}], 10)
    -> prompt: the instruction, a blank line, "[p1] Open 9 to 5.", a blank line,
       "Question: When is it open?\nAnswer:"   and used_ids ["p1"]

Trace by hand (which ids are used, and in which order?):

    passages = [{"id": "p1", "text": "a b c", "score": 0.9},
                {"id": "p2", "text": "a b c d e", "score": 0.7},
                {"id": "p3", "text": "a b", "score": 0.8}]
    build_rag_prompt("q?", passages, 6) -> used_ids ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify build_rag_prompt
"""

INSTRUCTION = (
    "Answer using only the passages below. Cite passage ids in square brackets, like [p1]. "
    "If the passages do not contain the answer, say: not in the documents."
)


def build_rag_prompt(question, passages, max_words):
    raise NotImplementedError
