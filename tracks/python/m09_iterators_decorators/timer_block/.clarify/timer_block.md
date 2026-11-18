# timer_block: clarifications

Pattern: context-manager

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- If the block raises, the exception must still propagate, and elapsed must still be set.
