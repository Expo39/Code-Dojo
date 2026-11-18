"""Dates in free text.

Level: easy
Target: 15

Write `find_dates(text)` that finds every date written as YYYY-MM-DD in `text`
and returns them as (year, month, day) tuples of ints, in the order they appear.
Use the `re` module.

    find_dates("Shipped 2024-03-15, delivered 2024-03-18.")
    -> [(2024, 3, 15), (2024, 3, 18)]

Trace by hand (work out the result yourself):

    find_dates("Invoice 2023-11-02 due 2023-12-01; paid 2024-01-07 by card") -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify find_dates
"""


def find_dates(text):
    raise NotImplementedError
