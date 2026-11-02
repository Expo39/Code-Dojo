"""A generator.

Level: easy
Target: 10
Pattern: generator

Write a generator function that yields lists of up to `size` items from any
iterable (it must work on an iterator that can only be read once, without
turning it into a list first).

    list(read_chunks(range(5), 2)) -> [[0, 1], [2, 3], [4]]

Read: https://docs.python.org/3/tutorial/classes.html#generators
"""


def read_chunks(iterable, size):
    raise NotImplementedError
