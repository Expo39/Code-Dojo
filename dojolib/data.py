"""The learner's records: log.csv, the redo schedule (Leitner boxes), timers and the
session clock, and the personal files every command expects."""

from __future__ import annotations

import csv
import shutil
from datetime import date, datetime, timedelta

from .core import (
    CHEATSHEET, CHEATSHEET_HEADER, INTERVALS, LOG, LOG_FIELDS, MISTAKES, MISTAKES_HEADER,
    PERSONAL_DOCS, PERSONAL_DOCS_INDEX, PROGRESS, REVIEWS, WEEKLY, die, fmt_date, now, parse_date,
    read_json, write_json
)


def ensure_files() -> None:
    PROGRESS.mkdir(exist_ok=True)
    migrate_log()
    WEEKLY.mkdir(exist_ok=True)
    (PROGRESS / "mocks").mkdir(exist_ok=True)
    (PROGRESS / "drills").mkdir(exist_ok=True)
    if not LOG.exists():
        with LOG.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(LOG_FIELDS)
    if not MISTAKES.exists():
        MISTAKES.write_text(MISTAKES_HEADER, encoding="utf-8")
    if not CHEATSHEET.exists():
        CHEATSHEET.write_text(CHEATSHEET_HEADER, encoding="utf-8")
    if not REVIEWS.exists():
        write_json(REVIEWS, {})
    PERSONAL_DOCS.mkdir(exist_ok=True)
    old_habits = PROGRESS / "WORK_HABITS.md"  # older checkouts kept it at the top of progress/
    if old_habits.exists() and not (PERSONAL_DOCS / "WORK_HABITS.md").exists():
        shutil.move(str(old_habits), PERSONAL_DOCS / "WORK_HABITS.md")
    index = PERSONAL_DOCS / "README.md"
    if not index.exists():
        index.write_text(PERSONAL_DOCS_INDEX, encoding="utf-8")


def migrate_log() -> None:
    """Rewrite an older log.csv with the current columns (new columns left empty)."""
    if not LOG.exists():
        return
    with LOG.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames == LOG_FIELDS:
            return
        rows = list(reader)
    with LOG.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in LOG_FIELDS})


def read_log() -> list[dict]:
    if not LOG.exists():
        return []
    with LOG.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_log(row: dict) -> None:
    ensure_files()
    with LOG.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writerow({k: row.get(k, "") for k in LOG_FIELDS})


def minutes_on(rows: list[dict], d: date) -> float:
    key = fmt_date(d)
    return sum(float(r["minutes"] or 0) for r in rows if r["date"] == key)


def minutes_between(rows: list[dict], start: date, end: date) -> float:
    total = 0.0
    for r in rows:
        d = parse_date(r["date"])
        if start <= d <= end:
            total += float(r["minutes"] or 0)
    return total


def schedule(item: str, result: str, ratio: float | None, hints: int, on: date) -> dict:
    """Update the Leitner box of an item after an attempt and return its card."""
    reviews = read_json(REVIEWS, {})
    card = reviews.get(item, {"box": 0, "attempts": 0, "clean": 0})
    card["attempts"] += 1
    if result != "solved":
        card["box"] = 0
        grade = "failed"
    elif hints == 0 and (ratio is None or ratio <= 1.0):
        card["box"] = min(card["box"] + 1, len(INTERVALS) - 1)
        card["clean"] += 1
        grade = "clean"
    elif hints <= 1 and (ratio is None or ratio <= 1.5):
        grade = "ok"
    else:
        card["box"] = 0
        grade = "struggled"
    card["last"] = fmt_date(on)
    card["grade"] = grade
    card["due"] = fmt_date(on + timedelta(days=INTERVALS[card["box"]]))
    reviews[item] = card
    write_json(REVIEWS, reviews)
    return card


def due_items(on: date) -> list[tuple[str, dict]]:
    reviews = read_json(REVIEWS, {})
    due = [(k, v) for k, v in reviews.items() if parse_date(v["due"]) <= on]
    return sorted(due, key=lambda kv: (parse_date(kv[1]["due"]), kv[1]["box"]))


def timer_of(value) -> dict:
    """Timers were plain start times in older versions; normalise to the dict form."""
    if isinstance(value, str):
        return {"start": value, "paused_total": 0.0, "paused_at": None}
    return value


def timer_minutes(value) -> float:
    t = timer_of(value)
    seconds = (now() - datetime.fromisoformat(t["start"])).total_seconds() - t["paused_total"]
    if t["paused_at"]:
        seconds -= (now() - datetime.fromisoformat(t["paused_at"])).total_seconds()
    return max(seconds, 0) / 60


def paused_minutes(value) -> float:
    """Minutes the clock was paused, including a pause still open."""
    t = timer_of(value)
    seconds = t["paused_total"]
    if t["paused_at"]:
        seconds += (now() - datetime.fromisoformat(t["paused_at"])).total_seconds()
    return seconds / 60


def pick_timer(timers: dict, item: str | None) -> str:
    if item:
        if item not in timers:
            die(f"No timer for '{item}'.")
        return item
    if len(timers) != 1:
        die("Name the timer: " + (", ".join(timers) if timers else "none running"))
    return next(iter(timers))


def session_gap(session: dict, rows: list[dict]) -> tuple[float, float, float]:
    """Session minutes so far, minutes logged since it started, and the gap between them."""
    clock = timer_minutes(session)
    logged = minutes_on(rows, parse_date(session["date"])) - session.get("logged_at_start", 0.0)
    return clock, logged, max(clock - logged, 0.0)
