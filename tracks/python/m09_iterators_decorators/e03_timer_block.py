"""A context manager.

Level: medium
Target: 20
Pattern: context-manager

Write a class Timer usable as `with Timer() as t: ...`. After the block,
t.elapsed holds the seconds the block took (use time.perf_counter). If the
block raises, the exception must still propagate and elapsed must still be set.

Read: https://docs.python.org/3/reference/datamodel.html#context-managers
"""


class Timer:
    pass
