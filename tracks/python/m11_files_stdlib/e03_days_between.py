"""Dates with datetime.

Level: easy
Target: 10

Given two ISO dates "YYYY-MM-DD", return the number of days from the first to the
second. Also write weekday_name(iso), returning "Monday", "Tuesday" and so on.

    days_between("2026-11-02", "2026-12-25") -> 53
    weekday_name("2026-11-02") -> "Monday"

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify days_between

Read: https://docs.python.org/3/library/datetime.html (date.fromisoformat, timedelta)
"""


def days_between(start, end):
    raise NotImplementedError


def weekday_name(iso):
    raise NotImplementedError
