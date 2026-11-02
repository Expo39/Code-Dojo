from datetime import date

NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def days_between(start, end):
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def weekday_name(iso):
    return NAMES[date.fromisoformat(iso).weekday()]
