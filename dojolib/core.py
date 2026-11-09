"""Paths, constants, file headers and small helpers shared by every module: dates, JSON,
minutes, prompts and the learner's profile."""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent  # the repository: dojolib/ sits next to dojo.py
TRACKS = ROOT / "tracks"
WORKSPACE = ROOT / "workspace"
PROGRESS = ROOT / "progress"
PROFILE = PROGRESS / "profile.json"
LOG = PROGRESS / "log.csv"
REVIEWS = PROGRESS / "reviews.json"
TIMER = PROGRESS / "timer.json"
SESSION = PROGRESS / "session.json"  # the session clock: training time between timers
MISTAKES = PROGRESS / "mistakes.md"
CHEATSHEET = PROGRESS / "cheatsheet.md"
WEEKLY = PROGRESS / "weekly"
SEEN = PROGRESS / "tracks_seen.json"  # exercise -> content hash the learner has already been asked about
TOPICS_SEEN = PROGRESS / "topics_seen.json"  # track/module -> lesson topics already asked about
UPSTREAM_CHECK = PROGRESS / "upstream_check.json"
PERSONAL_DOCS = PROGRESS / "docs"  # the learner's own docs, written by the tutor (docs/PERSONAL_DOCS.md)
# Inside each workspace module folder: earlier attempts, and PRIMM lesson scratch files.
HISTORY_DIR = ".history"
PRIMM_DIR = "primm"
LESSON_PREFIX = "lesson:"  # timer key of a PRIMM lesson, logged as study time by `done`

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
# Leitner boxes: days until the next redo. Box 4+ counts as mastered.
INTERVALS = [1, 3, 7, 14, 30, 60]
MASTERED_BOX = 4
TARGETS = {"tiny": 5, "easy": 15, "medium": 30, "hard": 45}
LOG_FIELDS = ["date", "item", "kind", "module", "pattern", "level",
              "minutes", "target", "hints", "result", "ratio", "skipped", "note"]
# The exercise loop (docs/CHECKLISTS.md). `done --skipped` records the steps left out.
STEPS = ["understand", "example", "plan", "predict", "test", "reflect"]
CHECKLIST = """Before typing:  1 understand (restate, ask about edge cases)  2 example (by hand)  3 plan (out loud, Big-O)
Before running: 4 predict (pass or fail? which test?)
After it runs:  5 test (trace your example, one edge case)  6 reflect (complexity, what would break it)"""
KINDS = ["exercise", "external", "mock", "drill", "study", "reading", "project"]

MODES = {
    "interview": "preparing for live-coding interviews (with or without a date)",
    "hybrid": "interview-ready and growing as an engineer at the same time",
    "industry": "preparing to enter an industry or role, no interview yet",
    "hobby": "for its own sake: building things, learning at your own pace",
}
LEVELS = {
    "hobbyist": "build your own things, read docs, fix your own bugs",
    "junior": "job-ready: everyday code fluently, read a team's code, tests, git",
    "mid": "design modules, review others' code, debug unfamiliar systems",
    "senior": "architecture, deep debugging and domain depth, guiding others",
}

DEFAULT_PROFILE = {
    "learner": "",
    "start_date": "",
    "target_date": "",
    "goal": "",
    "minutes": {"mon": 180, "tue": 180, "wed": 180, "thu": 180,
                "fri": 180, "sat": 180, "sun": 0},
    "flexible_rest_day": True,
    "level": "beginner",
    "start_module": "",
    "skip_modules": [],
    "skip_exercises": [],
    "tracks": [],
    # Share of new-material time per track (percent). 0 = maintenance: redos only, no new
    # material. Empty = the active tracks share equally. Set with `dojo.py mix`.
    "mix": {},
    # What overrides the mix right now, in words (e.g. "interview on 01/03/2027"), or empty.
    "priority": "",
    # Why they train and the programmer they want to become (docs/ROADMAP.md, section 1).
    "mode": "",
    "target_level": "",
    "export_target": "",
}

MISTAKES_HEADER = """# Mistakes log

One row per mistake. The tutor fills this in (`python dojo.py mistake ...`).
Read it at the end of each week; the weekly review turns repeats into drills.

| Date | Item | What went wrong | Correct form |
| --- | --- | --- | --- |
"""

PERSONAL_DOCS_INDEX = """# Your docs

Personal and local (gitignored). The shared docs in `docs/` describe the method for everyone;
these apply it to you. The tutor writes and updates them from your own data, following
`docs/PERSONAL_DOCS.md`; each is created only when it has something to say.

| File | What it holds | Updated |
| --- | --- | --- |
| `PITFALLS.md` | Your own recurring traps, from `progress/mistakes.md` | weekly review |
| `WEEK.md` | Your weekly rhythm: which day is for what, from your hours | placement, when hours change |
| `INTERVIEW_PREP.md` | Your interview goal: date, run-up plan, stories, questions | when an interview is a goal |
| `WORK_HABITS.md` | How training relates to your job, if you work in the field | placement, on request |
"""

CHEATSHEET_HEADER = """# Cheat sheet

Concepts worth reviewing, kept short by the tutor. One bullet per concept:
the idea in a few words, then "Check:" with a self-check question.
Mark mastered bullets with "(mastered DD/MM/YYYY)".

## Python syntax and built-ins

## Data structures

## Patterns and algorithms

## Debugging

## Interview technique
"""


def today() -> date:
    return date.today()


def now() -> datetime:
    return datetime.now().replace(microsecond=0)


# European dates everywhere the learner looks: DD/MM/YYYY in data and output, DD-MM-YYYY in
# file names, DD_MM_YYYY in names that must also be valid identifiers (popular_items_07_11_2026.py).
DATE_FMT = "%d/%m/%Y"
FILE_DATE_FMT = "%d-%m-%Y"
STAMP_FMT = "%d%m%Y_%H%M%S"


def fmt_date(d: date) -> str:
    return d.strftime(DATE_FMT)


def parse_date(text: str) -> date:
    """DD/MM/YYYY (also DD-MM-YYYY or DD.MM.YYYY); ISO YYYY-MM-DD is still read, for old data."""
    text = text.strip()
    m = re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})", text)
    if m:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return date.fromisoformat(text)


def week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def read_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def fmt_min(minutes: float) -> str:
    minutes = int(round(minutes))
    sign = "-" if minutes < 0 else ""
    h, m = divmod(abs(minutes), 60)
    return f"{sign}{h}h{m:02d}" if h else f"{sign}{m}m"


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    answer = input(f"{prompt}{suffix}: ").strip()
    return answer or default


def die(message: str) -> None:
    print(message)
    sys.exit(1)


def load_profile(required: bool = True) -> dict:
    profile = read_json(PROFILE, None)
    if profile is None:
        if required:
            die("No profile yet. Run: python dojo.py setup")
        return dict(DEFAULT_PROFILE)
    merged = dict(DEFAULT_PROFILE)
    merged.update(profile)
    return merged


def planned_minutes(profile: dict, d: date) -> int:
    start = profile.get("start_date")
    if start and d < parse_date(start):
        return 0
    return int(profile["minutes"].get(DAYS[d.weekday()], 0))


def weekly_target(profile: dict) -> int:
    return sum(int(profile["minutes"].get(day, 0)) for day in DAYS)
