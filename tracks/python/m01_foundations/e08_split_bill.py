"""Split a restaurant bill.

Level: easy
Target: 10

`split_bill(total, tip_percent, people)` adds a tip of `tip_percent` percent to the
bill `total`, rounds the result to the cent, and splits it between `people`
people. Return a list with one share per person, each a float rounded to cents.
The shares must add up exactly to the rounded total; any leftover cents go one
each to the first people in the list.

    split_bill(100, 15, 3) -> [38.34, 38.33, 38.33]

Trace by hand (work out the result yourself):

    split_bill(70, 10, 6) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify split_bill
"""


def split_bill(total, tip_percent, people):
    raise NotImplementedError
