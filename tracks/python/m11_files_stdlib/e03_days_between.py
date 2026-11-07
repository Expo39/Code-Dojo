"""Dates with datetime.

Level: easy
Target: 10

Given two dates written day first, "DD/MM/YYYY", return the number of days from the
first to the second. Also write weekday_name(day), returning "Monday", "Tuesday" and
so on.

    days_between("02/11/2026", "25/12/2026") -> 53
    weekday_name("02/11/2026") -> "Monday"

Trace by hand (work out the result yourself):

    days_between("25/12/2026", "01/01/2027") -> ?;  weekday_name("25/12/2026") -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify days_between

Read: https://docs.python.org/3/library/datetime.html (datetime.strptime, format codes, timedelta)
"""


def days_between(start, end):
    raise NotImplementedError


def weekday_name(day):
    raise NotImplementedError
