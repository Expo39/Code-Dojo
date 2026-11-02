"""A context manager.

Level: medium
Target: 20

Write a class Timer usable as `with Timer() as t: ...`. After the block, t.elapsed
holds the seconds the block took (measured with time.perf_counter).

    with Timer() as t: time.sleep(0.05)   ->  t.elapsed is about 0.05

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify timer_block

Read: https://docs.python.org/3/reference/datamodel.html#context-managers
"""


class Timer:
    pass
