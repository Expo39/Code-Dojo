"""Planning numbers: the strand balance, week figures, pattern stats, fluency gates, the
module overview, the track mix, confidence calibration and the interleaved redo order."""

from __future__ import annotations

import re
import statistics
from datetime import date, timedelta

from .core import REVIEWS, parse_date, planned_minutes, read_json, week_start, weekly_target
from .data import minutes_between, minutes_on
from .tracks import discover, load_tracks


# Target share of training time per strand, by mode (docs/METHOD.md, "The five strands").
STRAND_SHARES = {
    "interview": {"learn": 20, "write": 25, "read": 20, "build": 10, "perform": 25},
    "hybrid": {"learn": 25, "write": 25, "read": 20, "build": 15, "perform": 15},
    "industry": {"learn": 25, "write": 20, "read": 20, "build": 25, "perform": 10},
    "hobby": {"learn": 30, "write": 20, "read": 15, "build": 35, "perform": 0},
}
KIND_STRAND = {"study": "learn", "exercise": "write", "external": "write", "drill": "read",
               "reading": "read", "project": "build", "mock": "perform"}


def strand_split(rows: list[dict], start: date, end: date) -> dict:
    """Minutes per strand between two dates (inclusive)."""
    split = {k: 0.0 for k in STRAND_SHARES["interview"]}
    for r in rows:
        strand = KIND_STRAND.get(r["kind"])
        if strand and start <= parse_date(r["date"]) <= end:
            split[strand] += float(r["minutes"] or 0)
    return split


def strand_line(profile: dict, rows: list[dict], on: date) -> str | None:
    """Last 7 days by strand against the mode's shares, naming the strands that are short."""
    shares = STRAND_SHARES.get(profile.get("mode") or "interview", STRAND_SHARES["interview"])
    split = strand_split(rows, on - timedelta(days=6), on)
    total = sum(split.values())
    if total < 60:
        return None
    pct = {k: 100 * v / total for k, v in split.items()}
    parts = ", ".join(f"{k} {pct[k]:.0f}% ({shares[k]})" for k in shares)
    short = [k for k in shares if shares[k] - pct[k] >= 10]
    line = f"Last 7 days by strand, % (target): {parts}."
    if short:
        line += f" Short: {', '.join(short)}: do those blocks first today and never cut them."
    return line


def week_numbers(profile: dict, rows: list[dict], on: date) -> dict:
    start = week_start(on)
    done = minutes_between(rows, start, on)
    target = weekly_target(profile)
    # Days before today are due in full; today only counts once its plan is met.
    planned_before = sum(planned_minutes(profile, start + timedelta(days=i))
                         for i in range((on - start).days))
    done_today = minutes_on(rows, on)
    planned_today = planned_minutes(profile, on)
    gap = (done - done_today) - planned_before + max(0.0, done_today - planned_today)
    remaining_days = [start + timedelta(days=i) for i in range((on - start).days, 7)]
    planned_left = sum(planned_minutes(profile, d) for d in remaining_days)
    prev_start = start - timedelta(days=7)
    prev_done = minutes_between(rows, prev_start, start - timedelta(days=1))
    prev_target = sum(planned_minutes(profile, prev_start + timedelta(days=i)) for i in range(7))
    return {"start": start, "done": done, "target": target, "planned_so_far": planned_before,
            "gap": gap, "planned_left": planned_left,
            "prev_done": prev_done, "prev_gap": prev_done - prev_target,
            "remaining_days": [d for d in remaining_days if planned_minutes(profile, d) > 0]}


def recent_stats(rows: list[dict], days: int, on: date) -> dict:
    since = on - timedelta(days=days)
    attempts = [r for r in rows if r["kind"] in ("exercise", "external")
                and parse_date(r["date"]) > since and r["ratio"]]
    by_pattern: dict[str, list[dict]] = {}
    for r in attempts:
        by_pattern.setdefault(r["pattern"] or r["module"] or "other", []).append(r)
    out = {}
    for pattern, items in by_pattern.items():
        out[pattern] = {
            "n": len(items),
            "ratio": statistics.median(float(r["ratio"]) for r in items),
            "hints": statistics.mean(int(r["hints"] or 0) for r in items),
            "clean": sum(1 for r in items if r["result"] == "solved"
                         and int(r["hints"] or 0) == 0 and float(r["ratio"]) <= 1.0),
        }
    return out


MODULE_ROW_RE = re.compile(r"^\|\s*(m\d\d_[a-z0-9_]+)\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|\s*$", re.MULTILINE)


def module_overview(profile: dict) -> list[dict]:
    """Every module of the learner's tracks, in order, with the learner's status for it."""
    exercises = discover()
    reviews = read_json(REVIEWS, {})
    out = []
    for track_name, track in load_tracks(active_only=True).items():
        readme = track["dir"] / "README.md"
        focus = {m: (f, st) for m, f, st in MODULE_ROW_RE.findall(readme.read_text(encoding="utf-8"))} \
            if readme.exists() else {}
        on_disk = sorted({ex["module"] for ex in exercises.values() if ex["track"] == track_name})
        for module in sorted(set(on_disk) | set(focus)):
            slugs = [sl for sl, ex in exercises.items() if ex["track"] == track_name and ex["module"] == module]
            if any(module.startswith(x) for x in profile.get("skip_modules", [])):
                state = "excluded"
            elif not slugs:
                state = "planned"
            elif profile.get("start_module") and module < profile["start_module"]:
                state = "before start"
            else:
                state = "assigned"
            out.append({"track": track_name, "module": module, "focus": focus.get(module, ("", ""))[0],
                        "state": state, "total": len(slugs), "tried": sum(1 for sl in slugs if sl in reviews),
                        "note": profile.get("module_notes", {}).get(module, "")})
    return out


def print_modules(profile: dict) -> None:
    rows = module_overview(profile)
    for track in dict.fromkeys(r["track"] for r in rows):
        print(f"{track}:")
        for r in (x for x in rows if x["track"] == track):
            count = f"{r['tried']}/{r['total']}" if r["total"] else "   "
            note = f"  [your note: {r['note']}]" if r["note"] else ""
            print(f"  {r['state']:13} {r['module']:28} {count:6} {r['focus']}{note}")
    print("assigned = offered as new material; excluded = left out (redos still come back);")
    print("before start = before your start module; planned = no exercises yet, written when reached.")


def in_scope(ex: dict, profile: dict) -> bool:
    """False for modules the learner skipped or that come before their start module."""
    module = ex["module"]
    if any(module.startswith(s) for s in profile.get("skip_modules", [])):
        return False
    if ex["slug"] in profile.get("skip_exercises", []):
        return False
    start = profile.get("start_module", "")
    return not start or module >= start


def effective_mix(profile: dict) -> dict:
    """Map each active track -> its percent of new-material time (0 = maintenance)."""
    active = list(load_tracks(active_only=True))
    mix = {t: int(v) for t, v in (profile.get("mix") or {}).items() if t in active}
    if not mix:
        if not active:
            return {}
        share, rest = divmod(100, len(active))
        return {t: share + (1 if i < rest else 0) for i, t in enumerate(active)}
    full = {t: mix.get(t, 0) for t in active}
    return dict(sorted(full.items(), key=lambda kv: -kv[1]))  # largest share first


def next_new(profile: dict, limit: int = 3, track: str | None = None) -> list[dict]:
    reviews = read_json(REVIEWS, {})
    return [ex for slug, ex in discover().items()
            if slug not in reviews and in_scope(ex, profile)
            and (track is None or ex["track"] == track)][:limit]


def session_size(minutes: int) -> str:
    if minutes >= 150:
        return "full (3h)"
    if minutes >= 90:
        return "standard (2h)"
    if minutes >= 45:
        return "short (1h)"
    return "minimum (30m)"


def fluency_gates(rows: list[dict], on: date) -> list[tuple[str, bool]]:
    def last(n: int, levels: tuple[str, ...]) -> list[dict]:
        items = [r for r in rows if r["kind"] in ("exercise", "external", "mock")
                 and r["level"] in levels and r["ratio"]]
        return items[-n:]

    def gate(items: list[dict], n: int, max_ratio: float, max_hints: float) -> bool:
        return (len(items) >= n
                and statistics.median(float(r["ratio"]) for r in items) <= max_ratio
                and statistics.mean(int(r["hints"] or 0) for r in items) <= max_hints
                and all(r["result"] == "solved" for r in items))

    easy = last(10, ("tiny", "easy"))
    medium = last(8, ("medium",))
    mocks = [r for r in rows if r["kind"] == "mock"][-3:]
    return [
        ("Last 10 easy: all solved, median <= 1.2x target, <= 0.5 hints", gate(easy, 10, 1.2, 0.5)),
        ("Last 10 easy: median <= 1.0x target, 0 hints", gate(easy, 10, 1.0, 0.0)),
        ("Last 8 medium: all solved, median <= 1.3x target, <= 1 hint", gate(medium, 8, 1.3, 1.0)),
        ("Last 3 mocks passed", len(mocks) == 3 and all(r["result"] in ("pass", "strong") for r in mocks)),
    ]
def calibration(rows: list[dict]) -> list[str]:
    """Stated confidence against how often the prediction or answer was right."""
    items = []
    for r in rows:
        conf = r.get("confidence", "")
        if conf in ("", None):
            continue
        outcome = r.get("prediction") or ({"right": "right", "wrong": "wrong"}.get(r.get("result", "")))
        if outcome in ("right", "wrong"):
            items.append((float(conf), outcome == "right"))
    if not items:
        return []
    lines = []
    for lo, hi in ((0, 49), (50, 69), (70, 89), (90, 100)):
        band = [ok for c, ok in items if lo <= c <= hi]
        if band:
            said = statistics.mean(c for c, _ in items if lo <= c <= hi)
            lines.append(f"  said {lo}-{hi}%: n={len(band):<3} average said {said:.0f}%, "
                         f"actually right {100 * sum(band) / len(band):.0f}%")
    sure_wrong = sum(1 for c, ok in items if c >= 80 and not ok)
    if sure_wrong:
        lines.append(f"  confidently wrong (80%+ and wrong): {sure_wrong}: each is a misconception "
                     "worth a line in progress/mistakes.md")
    return lines


def interleave_due(due: list[tuple[str, dict]]) -> list[tuple[str, dict]]:
    """Redo order that switches pattern and module each time (retrieval from a cold start),
    taking the most overdue item of each group first."""
    exercises = discover()
    groups: dict[str, list[tuple[str, dict]]] = {}
    for item in due:
        ex = exercises.get(item[0], {})
        groups.setdefault(ex.get("pattern") or ex.get("module") or item[0], []).append(item)
    queues = sorted(groups.values(), key=lambda g: (parse_date(g[0][1]["due"]), g[0][1]["box"]))
    out: list[tuple[str, dict]] = []
    last_module = None
    while queues:
        idx = next((i for i, q in enumerate(queues)
                    if exercises.get(q[0][0], {}).get("module") != last_module), 0)
        queue = queues.pop(idx)
        item = queue.pop(0)
        last_module = exercises.get(item[0], {}).get("module")
        out.append(item)
        if queue:
            queues.append(queue)  # the group goes to the back: the next redo switches pattern
    return out

