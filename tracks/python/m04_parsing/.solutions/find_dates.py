import re

DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def find_dates(text):
    dates = []
    for year, month, day in DATE.findall(text):
        year, month, day = int(year), int(month), int(day)
        if 1 <= month <= 12 and 1 <= day <= 31:
            dates.append((year, month, day))
    return dates
