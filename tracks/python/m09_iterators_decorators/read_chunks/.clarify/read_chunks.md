# read_chunks: clarifications

Pattern: generator

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- It must work on an iterator that can only be read once, without turning it into a list first.
- The last chunk may be shorter; an empty iterable yields nothing.
- It must be a generator function (it uses yield).
