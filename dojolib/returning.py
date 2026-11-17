"""Coming back after time away: the `away` command, and the re-entry the brief shows while the
learner ramps back up (docs/DAILY_SESSION.md, "Coming back after time away").

The re-entry is worked out from two things: how long the learner was away, and how they used
to work before it (their own minutes per exercise and minutes per training day, from the log).
"""

from __future__ import annotations

import math
import statistics
from datetime import date, timedelta

from .core import (
    AWAY, AWAY_LONG_DAYS, AWAY_MIN_DAYS, AWAY_WEEK_DAYS, RETURNS, REVIEWS, day_runs, die, fmt_date,
    fmt_min, forget_away, inferred_away, parse_date, read_json, today, write_json
)

PACE_ITEMS = 20  # exercise attempts before the absence that set the usual minutes per item
PACE_DAYS = 28  # training days before the absence that set the usual minutes per day
DEFAULT_ITEM_MINUTES = 12.0  # no history yet
RUST_MAX = 1.5  # the most the targets stretch, reached at RUST_FULL_DAYS away
RUST_FULL_DAYS = 28
RAMP_MAX_DAYS = 4  # the ramp back to a full day: one day per week away, at most this many
FIRST_DAY_MIN = 0.5  # the first day back is never planned shorter than half a usual day
REDO_SHARE = 0.4  # share of a re-entry day for the redo queue (retrieval first)
MIN_REDOS = 3
LONG_DROP_BOX = 3  # after a long absence, overdue items from this box up drop one box (once)


def training_days(rows: list[dict]) -> list[date]:
    return sorted({parse_date(r["date"]) for r in rows if float(r["minutes"] or 0) > 0})


def latest_return(rows: list[dict], on: date) -> tuple[date, int, date] | None:
    """The most recent return: (first day back, days away, last training day before it).
    Today is the first day back when the last training day is AWAY_MIN_DAYS or more ago."""
    days = [d for d in training_days(rows) if d <= on]
    before = [d for d in days if d < on]
    if before and (on - before[-1]).days >= AWAY_MIN_DAYS:
        return on, (on - before[-1]).days, before[-1]
    for a, b in reversed(list(zip(days, days[1:]))):
        if (b - a).days >= AWAY_MIN_DAYS:
            return b, (b - a).days, a
    return None


def rust(days_away: int) -> float:
    """How much slower to expect: 1.0 just back, up to RUST_MAX after RUST_FULL_DAYS away."""
    return round(1 + (RUST_MAX - 1) * min(days_away, RUST_FULL_DAYS) / RUST_FULL_DAYS, 2)


def ramp_days(days_away: int) -> int:
    return min(RAMP_MAX_DAYS, math.ceil(days_away / 7))


def usual_pace(rows: list[dict], before: date) -> tuple[float, float]:
    """Median minutes per exercise attempt and per training day, before the absence."""
    earlier = [r for r in rows if parse_date(r["date"]) < before]
    attempts = [float(r["minutes"]) for r in earlier
                if r["kind"] in ("exercise", "external") and r["ratio"] and float(r["minutes"] or 0) > 0]
    per_item = statistics.median(attempts[-PACE_ITEMS:]) if attempts else DEFAULT_ITEM_MINUTES
    per_day: dict[date, float] = {}
    for r in earlier:
        per_day[parse_date(r["date"])] = per_day.get(parse_date(r["date"]), 0.0) + float(r["minutes"] or 0)
    days = [m for _, m in sorted(per_day.items()) if m > 0][-PACE_DAYS:]
    return per_item, (statistics.median(days) if days else 0.0)


def reentry(rows: list[dict], on: date, plan: int) -> dict | None:
    """Today's re-entry while the ramp lasts, else None. Keys: day, of, away, back, last, rust,
    minutes (suggested today), redos (cap), per_item, per_day."""
    found = latest_return(rows, on)
    if not found:
        return None
    back, away, last = found
    ramp = ramp_days(away)
    day = (on - back).days + 1
    if day > ramp:
        return None
    per_item, per_day = usual_pace(rows, back)
    base = min(plan, per_day) if per_day else plan
    first = max(FIRST_DAY_MIN, 1 - away / RUST_FULL_DAYS)
    fraction = first + (1 - first) * (day - 1) / ramp
    minutes = base * fraction
    factor = rust(away)
    redos = max(MIN_REDOS, int(REDO_SHARE * minutes // (per_item * factor))) if minutes else MIN_REDOS
    return {"day": day, "of": ramp, "away": away, "back": back, "last": last, "rust": factor,
            "minutes": minutes, "redos": redos, "per_item": per_item, "per_day": per_day}


def rust_allowance(rows: list[dict], on: date) -> float:
    """The target stretch for a redo done today: above 1.0 only during a re-entry ramp."""
    found = latest_return(rows, on)
    if not found:
        return 1.0
    back, away, _ = found
    return rust(away) if (on - back).days + 1 <= ramp_days(away) else 1.0


def reentry_queue(due: list[tuple[str, dict]], cap: int) -> tuple[list[tuple[str, dict]], int]:
    """The redo queue capped at `cap`, lowest boxes first (kept in the interleaved order);
    returns today's items and how many wait for the coming days."""
    if not cap or len(due) <= cap:
        return due, 0
    keep = {k for k, _ in sorted(due, key=lambda kv: kv[1]["box"])[:cap]}
    return [kv for kv in due if kv[0] in keep], len(due) - cap


def drop_overdue_boxes(on: date, last: date) -> list[str]:
    """After a long absence, overdue items in box LONG_DROP_BOX or higher drop one box, due today.
    Runs once per return (keyed by the last training day before it)."""
    done = read_json(RETURNS, {})
    key = fmt_date(last)
    if done.get("boxes_dropped") == key:
        return done.get("dropped", [])
    reviews = read_json(REVIEWS, {})
    dropped = []
    for item, card in reviews.items():
        if card["box"] >= LONG_DROP_BOX and parse_date(card["due"]) < on:
            card["box"] -= 1
            card["due"] = fmt_date(on)
            dropped.append(item)
    if dropped:
        write_json(REVIEWS, reviews)
    write_json(RETURNS, {"boxes_dropped": key, "dropped": dropped})
    return dropped


def return_lines(profile: dict, r: dict, on: date) -> list[str]:
    """The brief's re-entry block, from the days away and the learner's usual pace."""
    head = (f"Back after {r['away']} days (last training {fmt_date(r['last'])})"
            if r["day"] == 1 else f"Re-entry day {r['day']} of {r['of']} (back after {r['away']} days)")
    lines = [f"{head}. Time away is not owed: no catch-up, and the days away plan nothing."]
    pace = (f"your usual pace before the break: {fmt_min(r['per_item'])} an exercise, "
            f"{fmt_min(r['per_day'])} a day" if r["per_day"] else "no pace history yet")
    steps = [f"about {fmt_min(r['minutes'])} today" + (f" (day {r['day']} of a {r['of']}-day ramp)" if r["of"] > 1 else ""),
             f"the redo queue first, at most {r['redos']} items, lowest boxes first",
             f"targets stretched x{r['rust']} for rust (time only; hints and failures count as usual)"]
    if r["day"] == 1 and r["away"] >= AWAY_WEEK_DAYS:
        steps.append("no new material today")
    if r["day"] == 1 and r["away"] >= AWAY_LONG_DAYS:
        steps.append("before new material starts again, a short probe on the concepts marked held (dojo-probe)")
    lines.append(f"  Re-entry ({pace}): " + "; ".join(steps) + ".")
    if r["away"] >= AWAY_LONG_DAYS:
        dropped = drop_overdue_boxes(on, r["last"])
        if dropped and r["day"] == 1:
            lines.append(f"  Overdue items from box {LONG_DROP_BOX} up dropped one box: {', '.join(dropped)}.")
        if profile.get("target_date") and r["day"] == 1:
            lines.append("  Roadmap trigger: a long absence with a target date. Check the date still "
                         "holds (dojo-roadmap).")
    return lines


def cmd_away(args) -> None:
    """Record time away (illness, holiday, a busy week), list it, or remove a period."""
    periods = read_json(AWAY, [])
    if args.remove:
        start = parse_date(args.remove)
        kept = [p for p in periods if parse_date(p["from"]) != start]
        if len(kept) == len(periods):
            die(f"No recorded period starts on {fmt_date(start)}.")
        write_json(AWAY, kept)
        forget_away()
        print(f"Removed the period from {fmt_date(start)}.")
        return
    if args.dates:
        if len(args.dates) > 2:
            die("Give one date, or a first and a last date: away 12/11/2026 16/11/2026")
        first = parse_date(args.dates[0])
        last = parse_date(args.dates[-1])
        if last < first:
            die("The last date comes before the first.")
        periods.append({"from": fmt_date(first), "to": fmt_date(last), "reason": args.reason or ""})
        periods.sort(key=lambda p: parse_date(p["from"]))
        write_json(AWAY, periods)
        forget_away()
        days = (last - first).days + 1
        print(f"Recorded {days} day(s) away, {fmt_date(first)} to {fmt_date(last)}"
              + (f" ({args.reason})" if args.reason else "")
              + ": those days plan no time, so nothing is owed for them.")
    on = today()
    if periods:
        print("Recorded time away:")
        for p in periods:
            print(f"  {p['from']} to {p['to']}" + (f"  {p['reason']}" if p.get("reason") else ""))
    recorded = {d for p in periods for d in _span(p)}
    inferred = [r for r in day_runs(inferred_away(on) - recorded) if (on - r[1]).days <= 90]
    if inferred:
        print(f"Read from the log ({AWAY_MIN_DAYS}+ days without training, last 90 days):")
        for a, b in inferred:
            print(f"  {fmt_date(a)} to {fmt_date(b)}")
    if not periods and not inferred:
        print("No time away recorded or read from the log.")


def _span(period: dict) -> list[date]:
    first, last = parse_date(period["from"]), parse_date(period["to"])
    return [first + timedelta(days=i) for i in range((last - first).days + 1)]
