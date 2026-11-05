"""A generator.

Level: easy
Target: 10

Write a generator function that yields lists of up to `size` items from any
iterable.

    list(read_chunks(range(5), 2)) -> [[0, 1], [2, 3], [4]]

Trace by hand (work out the result yourself):

    list(read_chunks("abcdefg", 3)) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify read_chunks

Read: https://docs.python.org/3/tutorial/classes.html#generators
"""


def read_chunks(iterable, size):
    raise NotImplementedError
