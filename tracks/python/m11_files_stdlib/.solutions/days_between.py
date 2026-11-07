from datetime import datetime

NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def parse(day):
    return datetime.strptime(day, "%d/%m/%Y").date()


def days_between(start, end):
    return (parse(end) - parse(start)).days


def weekday_name(day):
    return NAMES[parse(day).weekday()]
