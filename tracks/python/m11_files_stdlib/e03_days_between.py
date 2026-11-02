"""Dates with datetime.

Level: easy
Target: 10
Pattern: datetime

Given two ISO dates "YYYY-MM-DD", return the number of days from the first to
the second (negative if the second is earlier). Also write
weekday_name(iso) -> "Monday" etc. Invalid dates raise ValueError (let
datetime raise it).

    days_between("2026-11-02", "2026-12-25") -> 53
    weekday_name("2026-11-02") -> "Monday"

Read: https://docs.python.org/3/library/datetime.html (date.fromisoformat, timedelta)
"""


def days_between(start, end):
    raise NotImplementedError


def weekday_name(iso):
    raise NotImplementedError
