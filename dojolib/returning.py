"""Coming back after time away: the `away` command, and the re-entry the brief shows on the
first day back (docs/DAILY_SESSION.md, "Coming back after time away")."""

from __future__ import annotations

from datetime import date, timedelta

from .core import (
    AWAY, AWAY_LONG_DAYS, AWAY_MIN_DAYS, AWAY_WEEK_DAYS, RETURNS, REVIEWS, day_runs, die, fmt_date,
    fmt_min, forget_away, inferred_away, parse_date, read_json, today, write_json
)

REENTRY_REDOS = 6  # redo items on the first day back, lowest boxes first; the rest follow over the week
LONG_DROP_BOX = 3  # after a long absence, overdue items from this box up drop one box (once)


def last_training_day(rows: list[dict], on: date) -> date | None:
    days = [parse_date(r["date"]) for r in rows if float(r["minutes"] or 0) > 0]
    days = [d for d in days if d < on]
    return max(days) if days else None


def days_back(rows: list[dict], on: date) -> tuple[int, date | None]:
    """Days since the last training day before today, when that counts as a return (else 0)."""
    last = last_training_day(rows, on)
    if last is None:
        return 0, None
    gap = (on - last).days
    return (gap, last) if gap >= AWAY_MIN_DAYS else (0, last)


def reentry_queue(due: list[tuple[str, dict]], gap: int) -> tuple[list[tuple[str, dict]], int]:
    """On the first day back, the redo queue capped at REENTRY_REDOS, lowest boxes first (kept in
    the interleaved order); returns today's items and how many wait for the coming days."""
    if not gap or len(due) <= REENTRY_REDOS:
        return due, 0
    keep = {k for k, _ in sorted(due, key=lambda kv: kv[1]["box"])[:REENTRY_REDOS]}
    return [kv for kv in due if kv[0] in keep], len(due) - REENTRY_REDOS


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


def return_lines(profile: dict, gap: int, last: date, plan: int, on: date) -> list[str]:
    """The brief's re-entry block on the first day back, scaled by how long the learner was away."""
    lines = [f"Back after {gap} days (last training {fmt_date(last)}). Time away is not owed: "
             "no catch-up, and the days away plan nothing."]
    steps = [f"the redo queue first, capped at {REENTRY_REDOS} items, lowest boxes first"]
    if gap >= AWAY_WEEK_DAYS:
        steps.append(f"a short session (about {fmt_min(plan / 2)} is enough)" if plan else "a short session")
        steps.append("no new material today")
    if gap >= AWAY_LONG_DAYS:
        steps.append("before new material starts again, a short probe on the concepts marked held (dojo-probe)")
    lines.append("  Re-entry today: " + "; ".join(steps) + ".")
    if gap >= AWAY_LONG_DAYS:
        dropped = drop_overdue_boxes(on, last)
        if dropped:
            lines.append(f"  Overdue items from box {LONG_DROP_BOX} up dropped one box: {', '.join(dropped)}.")
        if profile.get("target_date"):
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
