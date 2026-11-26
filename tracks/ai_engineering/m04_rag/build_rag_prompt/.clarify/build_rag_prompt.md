# build_rag_prompt: clarifications

Pattern: budgeted-selection

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Words are counted by splitting each passage text on whitespace; the instruction and the question do not count.
- Highest score first; equal scores keep their order in the input.
- A passage that does not fit is skipped, and later (lower-scored, smaller) ones are still tried.
- The total of the chosen passages may equal `max_words` exactly.
- The passages in the prompt, and in `used_ids`, are in score order, not input order.
- No passage chosen: the passage block is left out entirely, so there is no extra blank line.
- Do not change the passages list or its dicts.
