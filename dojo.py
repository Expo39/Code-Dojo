#!/usr/bin/env python3
"""Code Dojo: tracker, scheduler and exercise runner.

Standard library only, works on Linux, macOS and Windows.
Run `python dojo.py help` for the commands (use `python3` on Linux/macOS if
`python` is not found).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRACKS = ROOT / "tracks"
WORKSPACE = ROOT / "workspace"
PROGRESS = ROOT / "progress"
PROFILE = PROGRESS / "profile.json"
LOG = PROGRESS / "log.csv"
REVIEWS = PROGRESS / "reviews.json"
TIMER = PROGRESS / "timer.json"
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
    # What overrides the mix right now, in words (e.g. "interview on 2027-03-01"), or empty.
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
Mark mastered bullets with "(mastered YYYY-MM-DD)".

## Python syntax and built-ins

## Data structures

## Patterns and algorithms

## Debugging

## Interview technique
"""


# --------------------------------------------------------------------- utils

def today() -> date:
    return date.today()


def now() -> datetime:
    return datetime.now().replace(microsecond=0)


def parse_date(text: str) -> date:
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


# ------------------------------------------------------------------- profile

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


NEXT_STEPS = """
What happens next
  Open the tutor in this folder (`claude`, `codex` or `gemini`) and say:  assess me
  The tutor then:
    - asks about your background and your goals (what, why, how far is enough, any date),
      and imports notes or old logs you point it to;
    - gives a short practical check to find your real starting point;
    - writes your plan (progress/PLAN.md: roadmap, skill tree, milestones from your own pace),
      your baseline, and your own docs (progress/docs/);
    - starts the first session. From then on, just say hello at the start of each session.
  Everything you need to say to it: docs/TUTOR.md. Without the tutor: python dojo.py help.
"""


def parse_minutes(text: str, current: dict) -> dict:
    """'60' sets every day; 'mon=60,sat=0' sets those days and keeps the rest."""
    text = str(text).strip()
    if text.isdigit():
        return {day: int(text) for day in DAYS}
    minutes = dict(current)
    for part in text.split(","):
        day, _, value = part.strip().partition("=")
        day = day.strip().lower()[:3]
        if day not in DAYS or not value.strip().isdigit():
            die(f"Minutes: use a number, or day=minutes pairs like mon=60,sat=0 (got '{part}').")
        minutes[day] = int(value)
    return minutes


# key -> (kind, allowed values or None, meaning). The mix and priority have `dojo.py mix`.
SETTINGS = {
    "learner": ("text", None, "your name"),
    "goal": ("text", None, "your goal in one line"),
    "mode": ("choice", MODES, "why you train"),
    "target_level": ("choice", LEVELS, "the programmer you want to become"),
    "level": ("choice", {"beginner": "", "intermediate": "", "advanced": ""}, "where you are now"),
    "start_date": ("date", None, "first training day"),
    "target_date": ("date", None, "a date to be ready by (empty for none)"),
    "minutes": ("minutes", None, "minutes per day: 60 for every day, or mon=60,sat=0"),
    "flexible_rest_day": ("bool", None, "training on a rest day counts towards the week"),
    "tracks": ("list", None, "tracks you follow"),
    "start_module": ("text", None, "first module offered as new material"),
    "skip_modules": ("list", None, "modules not offered as new material"),
    "skip_exercises": ("list", None, "single exercises not offered as new material"),
    "export_target": ("text", None, "where `export` sends backups"),
}


def show_value(profile: dict, key: str) -> str:
    value = profile.get(key)
    if key == "minutes":
        return ", ".join(f"{d}={value.get(d, 0)}" for d in DAYS)
    if isinstance(value, list):
        return ",".join(value) or "(none)"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value) if value not in ("", None) else "(empty)"


def set_setting(profile: dict, key: str, raw: str) -> None:
    if key not in SETTINGS:
        die(f"Unknown setting '{key}'. Settings: {', '.join(SETTINGS)} (mix and priority: dojo.py mix).")
    kind, allowed, _ = SETTINGS[key]
    raw = raw.strip()
    if kind == "choice":
        if raw not in allowed:
            die(f"{key}: one of {', '.join(allowed)}.")
        profile[key] = raw
    elif kind == "date":
        if raw:
            parse_date(raw)
        profile[key] = raw
    elif kind == "minutes":
        profile[key] = parse_minutes(raw, profile["minutes"])
    elif kind == "bool":
        profile[key] = raw.lower() in ("y", "yes", "true", "1")
    elif kind == "list":
        items = [x.strip() for x in raw.split(",") if x.strip()]
        if key == "tracks":
            unknown = [t for t in items if t not in load_tracks(active_only=False)]
            if unknown:
                die(f"Unknown track(s): {', '.join(unknown)}.")
        profile[key] = items
    else:
        profile[key] = raw


def settings_review(profile: dict) -> list[str]:
    """Evidence-based suggestions from the last 4 full weeks; the tutor asks yes or no for each."""
    rows = read_log()
    on = today()
    this_week = week_start(on)
    start = parse_date(profile["start_date"]) if profile.get("start_date") else this_week - timedelta(days=28)
    weeks = [this_week - timedelta(days=7 * i) for i in range(4, 0, -1)
             if this_week - timedelta(days=7 * i) >= week_start(start)]
    out = []
    if len(weeks) < 2:
        out.append(f"Only {len(weeks)} full week(s) of data: too early for time suggestions.")
    else:
        for i, day in enumerate(DAYS):
            done = [minutes_on(rows, w + timedelta(days=i)) for w in weeks]
            plan = int(profile["minutes"].get(day, 0))
            real = statistics.median(done)
            if abs(real - plan) >= 30 and abs(real - plan) >= 0.25 * max(plan, 1):
                suggestion = int(round(real / 15) * 15)
                out.append(f"minutes {day}: planned {plan}, median {real:.0f} over the last "
                           f"{len(weeks)} weeks -> suggest `settings minutes={day}={suggestion}`")
    if profile.get("target_date") and parse_date(profile["target_date"]) < on:
        out.append(f"target_date {profile['target_date']} has passed -> suggest clearing it "
                   "(`settings target_date=`) or setting the next one")
    mix = effective_mix(profile)
    if len(mix) > 1:
        module_track = {ex["module"]: ex["track"] for ex in discover().values()}
        since = on - timedelta(days=14)
        spent: dict[str, float] = {}
        for r in rows:
            if parse_date(r["date"]) > since and r["module"] in module_track:
                spent[module_track[r["module"]]] = spent.get(module_track[r["module"]], 0.0) + float(r["minutes"] or 0)
        total = sum(spent.values())
        for t, v in mix.items():
            real = 100 * spent.get(t, 0) / total if total else 0
            if total and abs(real - v) > 15:
                out.append(f"mix {t}: planned {v}%, real {real:.0f}% over 14 days -> keep the mix and "
                           "follow it, or change it (`mix ...`): ask which")
    out.append("Judgement calls to ask about (no numbers decide these): mode, target_level, priority, "
               "tracks, skip_modules (see PLAN.md, the weekly report and the roadmap triggers).")
    return out


def cmd_settings(args) -> None:
    """Show every setting, change any of them (key=value), or suggest changes from the log."""
    profile = load_profile()
    if args.review:
        print("Suggested changes (ask the learner yes or no for each; apply only the yes ones):")
        for line in settings_review(profile):
            print("  - " + line)
        return
    if args.changes:
        before = {k: show_value(profile, k) for k in SETTINGS}
        for change in args.changes:
            key, sep, raw = change.partition("=")
            if not sep:
                die(f"Use key=value, or key+=value to add to a list (got '{change}').")
            key = key.strip()
            if key.endswith(("+", "-")):  # key+=a adds to a list setting, key-=a removes from it
                op, key = key[-1], key[:-1].strip()
                if SETTINGS.get(key, ("",))[0] != "list":
                    die(f"+= and -= work only for list settings ({', '.join(k for k, v in SETTINGS.items() if v[0] == 'list')}).")
                given = [x.strip() for x in raw.split(",") if x.strip()]
                current = list(profile.get(key, []))
                kept = [x for x in current if x not in given] if op == "-" else current + [x for x in given if x not in current]
                raw = ",".join(kept)
            set_setting(profile, key, raw)
        notes = profile.get("module_notes", {})
        for module in [m for m in notes if not any(m.startswith(x) for x in profile.get("skip_modules", []))]:
            notes.pop(module)  # back in scope: the reason for leaving it out no longer applies
        write_json(PROFILE, profile)
        for k in SETTINGS:
            after = show_value(profile, k)
            if after != before[k]:
                print(f"  {k}: {before[k]} -> {after}")
        print("Saved. Note the reason under 'Plan changes' in progress/PLAN.md.")
        return
    for key, (_, _, meaning) in SETTINGS.items():
        print(f"  {key:18} {show_value(profile, key)}   ({meaning})")
    print(f"  {'mix':18} {', '.join(f'{t}={v}' for t, v in effective_mix(profile).items())}   (share per track: dojo.py mix)")
    print(f"  {'priority':18} {profile.get('priority') or '(none)'}   (what overrides the mix: dojo.py mix --priority)")
    print("Change: python dojo.py settings key=value ...   Suggestions: python dojo.py settings --review")


def ensure_git_hooks() -> str:
    """Turn on the shared pre-push checks (.githooks/pre-push runs tools/check.py)."""
    if not (ROOT / ".git").exists() or not (ROOT / ".githooks" / "pre-push").exists():
        return "Pre-push checks: not a git clone, skipped."
    current = subprocess.run(["git", "-C", str(ROOT), "config", "core.hooksPath"],
                             capture_output=True, text=True).stdout.strip()
    if current == ".githooks":
        return "Pre-push checks: on (.githooks/pre-push)"
    subprocess.run(["git", "-C", str(ROOT), "config", "core.hooksPath", ".githooks"])
    return "Pre-push checks: turned on (.githooks/pre-push runs tools/check.py before every push)"


def needs_install() -> bool:
    py = find_venv_python()
    if py is None:
        return True
    return subprocess.run([str(py), "-c", "import pytest"], capture_output=True).returncode != 0


def cmd_setup(args) -> None:
    """One command for a new learner: install if needed, ask (or take flags), check, explain."""
    quiet = args.yes  # the tutor passes --yes with flags after asking the learner in chat

    def value(flag, prompt: str, default: str) -> str:
        if flag is not None:
            return str(flag)
        return default if quiet else ask(prompt, default)

    if needs_install():
        print("First run: creating .venv and installing pytest ...")
        cmd_install(args)
    existing = read_json(PROFILE, None)
    if existing and not args.fresh and not quiet:
        print(f"Profile found for '{existing.get('learner')}'.")
        if ask("Is this you? (y/n)", "y").lower().startswith("n"):
            print("Run `python dojo.py setup --fresh` to archive that progress and start clean.")
            return
        print("Editing the existing profile (press Enter to keep a value).")
    if args.fresh and (PROGRESS.exists() and any(PROGRESS.iterdir())):
        stamp = now().strftime("%Y%m%d_%H%M%S")
        archive = ROOT / f"progress_archive_{stamp}"
        shutil.move(str(PROGRESS), archive)
        if WORKSPACE.exists() and any(p for p in WORKSPACE.iterdir() if p.name != ".gitkeep"):
            shutil.move(str(WORKSPACE), archive / "workspace")
        print(f"Old progress moved to {archive.name}/ (delete it once you no longer need it).")
        existing = None

    profile = dict(DEFAULT_PROFILE)
    if existing:
        profile.update(existing)

    if not quiet:
        print("\nCode Dojo setup: a few questions, then a check, then what to do next.")
        print("Everything can be changed later (run this again, or tell the tutor).\n")
    profile["learner"] = value(args.name, "Your name",
                               profile["learner"] or os.environ.get("USER", os.environ.get("USERNAME", "")))
    profile["goal"] = value(args.goal, "Your goal in one line (the tutor refines it with you)", profile["goal"])
    if not quiet:
        print("\nWhy are you training? (It sets how much interview practice you get.)")
        for key, text in MODES.items():
            print(f"  {key:10} {text}")
    mode = value(args.mode, "Mode", profile["mode"] or "hybrid").strip().lower()
    profile["mode"] = mode if mode in MODES else (profile["mode"] or "hybrid")
    if not quiet:
        print("\nWhat kind of programmer do you want to become? (It sets how far each goal goes.)")
        for key, text in LEVELS.items():
            print(f"  {key:10} {text}")
    level = value(args.target_level, "Target level", profile["target_level"] or "junior").strip().lower()
    profile["target_level"] = level if level in LEVELS else (profile["target_level"] or "junior")
    profile["start_date"] = value(args.start_date, "Start date (YYYY-MM-DD)",
                                  profile["start_date"] or today().isoformat())
    profile["target_date"] = value(args.target_date, "Target date, e.g. an interview (YYYY-MM-DD, empty for none)",
                                   profile["target_date"])

    minutes = dict(profile["minutes"])
    if args.minutes is not None or quiet:
        if args.minutes is not None:
            minutes = parse_minutes(args.minutes, minutes)
            for day in [r.strip().lower()[:3] for r in (args.rest or "").split(",") if r.strip()]:
                if day in minutes:
                    minutes[day] = 0
    else:
        print("\nHow many minutes can you train on each day? 0 = rest day.")
        print("Tip: enter one number for every day (e.g. 60), then adjust single days.")
        same = ask("Minutes for every day (empty to set day by day)", "")
        if same:
            minutes = {day: int(same) for day in DAYS}
            rest = ask("Rest days, comma separated (e.g. sun or sat,sun; empty for none)", "sun")
            for day in [r.strip().lower()[:3] for r in rest.split(",") if r.strip()]:
                if day in minutes:
                    minutes[day] = 0
        else:
            for day in DAYS:
                minutes[day] = int(ask(f"  {day}", str(minutes.get(day, 0))))
    profile["minutes"] = minutes
    flex = value(args.flexible, "Flexible rest day? Training on a rest day counts towards the week (y/n)",
                 "y" if profile["flexible_rest_day"] else "n")
    profile["flexible_rest_day"] = flex.lower().startswith("y")

    available = load_tracks(active_only=False)
    if not quiet:
        print("\nTracks available: " + ", ".join(f"{k} ({v['name']})" for k, v in available.items()))
        print("(Several tracks, or one you want that is not here yet? The tutor plans that with you.)")
    chosen = value(args.tracks, "Tracks to follow, comma separated (empty = all)", ",".join(profile["tracks"]))
    profile["tracks"] = [t.strip() for t in chosen.split(",") if t.strip() in available]
    if len(profile["tracks"]) > 1 and not quiet:
        print("\nSeveral tracks: how should new-material time be shared? Percent per track,")
        print("summing to 100; 0 = redos only (maintenance). The tutor can plan this with you.")
        current = effective_mix(profile)
        mix = {t: int(ask(f"  {t} %", str(current.get(t, 0)))) for t in profile["tracks"]}
        if sum(mix.values()) == 100:
            profile["mix"] = mix
        else:
            print("  Not 100 in total: kept the previous mix. Change it later with `dojo.py mix`.")
    if not quiet:
        print("\nWhere are you now? The tutor's placement (`assess me`) checks this properly.")
        print("  beginner     = new to writing code by hand")
        print("  intermediate = can write small programs, slow or needs hints")
        print("  advanced     = fluent in the basics, here for patterns and interviews")
    profile["level"] = value(args.level, "Level", profile["level"])

    PROGRESS.mkdir(exist_ok=True)
    WORKSPACE.mkdir(exist_ok=True)
    write_json(PROFILE, profile)
    ensure_files()
    total = weekly_target(profile)
    print(f"\nSaved. Weekly target: {fmt_min(total)} over "
          f"{sum(1 for d in DAYS if minutes[d] > 0)} days.\n")
    cmd_doctor(args)
    print("\nYour modules for now (all of your tracks; placement may move your start point):\n")
    print_modules(profile)
    if not quiet:
        print("\nAnything you want to leave out already? Give a short reason for each: the tutor")
        print("goes through them with you in placement and you decide together.")
        out = ask("Modules to leave out, comma separated (empty = none, decide in placement)", "")
        notes = dict(profile.get("module_notes", {}))
        known = {r["module"] for r in module_overview(profile)}
        for module in [m.strip() for m in out.split(",") if m.strip()]:
            if module not in known:
                print(f"  Unknown module '{module}', skipped.")
                continue
            notes[module] = "wants it left out: " + ask(f"  Why leave out {module}?", "no reason given")
            if module not in profile["skip_modules"]:
                profile["skip_modules"].append(module)
        if notes:
            profile["module_notes"] = notes
            write_json(PROFILE, profile)
            print("Noted. The tutor will ask about these in placement.")
    print(NEXT_STEPS)


def ensure_files() -> None:
    PROGRESS.mkdir(exist_ok=True)
    migrate_log()
    WEEKLY.mkdir(exist_ok=True)
    (PROGRESS / "mocks").mkdir(exist_ok=True)
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


# ----------------------------------------------------------------- exercises

HEADER_RE = re.compile(r"^\s*(?:#|//|--|\*|;)?\s*(Level|Target|Pattern|Kind):\s*(.+?)\s*$", re.MULTILINE)
STUB_RE = re.compile(r"^[a-z]\d\d_([a-z0-9_]+)(\.[A-Za-z0-9]+)$")
DEFAULT_TRACK = {
    "name": "",
    "extension": ".py",
    "test_file": "tests/test_{slug}.py",
    "solution_file": ".solutions/{slug}.py",
    "clarify_file": ".clarify/{slug}.md",
    "test_command": None,
    # What a learner should have before starting this track, in words (docs/ROADMAP.md).
    "requires": [],
    # When the track was last checked against current courses and the current version (YYYY-MM-DD).
    "reviewed": "",
}


def load_tracks(active_only: bool = True) -> dict:
    """Map track folder name -> its track.json settings."""
    tracks = {}
    for config in sorted(TRACKS.glob("*/track.json")):
        settings = dict(DEFAULT_TRACK)
        settings.update(read_json(config, {}))
        settings["dir"] = config.parent
        settings["name"] = settings["name"] or config.parent.name
        tracks[config.parent.name] = settings
    if active_only:
        chosen = read_json(PROFILE, {}).get("tracks") or []
        if chosen:
            tracks = {k: v for k, v in tracks.items() if k in chosen}
    return tracks


def discover(active_only: bool = True) -> dict:
    """Map slug -> exercise metadata, in syllabus order, for the learner's tracks."""
    found = {}
    for track_name, track in load_tracks(active_only).items():
        ext = track["extension"]
        for path in sorted(track["dir"].rglob(f"*{ext}")):
            if any(part.startswith(".") or part in ("tests", PRIMM_DIR)
                   for part in path.relative_to(track["dir"]).parts[:-1]):
                continue
            m = STUB_RE.match(path.name)
            if not m or m.group(2) != ext:
                continue
            slug = m.group(1)
            if slug in found:
                print(f"Warning: exercise name '{slug}' is used twice; keeping {found[slug]['stub']}")
                continue
            text = path.read_text(encoding="utf-8")
            meta = {k.lower(): v.strip() for k, v in HEADER_RE.findall(text)}
            clarify = path.parent / track["clarify_file"].format(slug=slug)
            if clarify.exists():
                # The pattern lives in the hidden clarify file so the task does not give it away.
                hidden = {k.lower(): v.strip() for k, v in HEADER_RE.findall(clarify.read_text(encoding="utf-8"))}
                meta = {**hidden, **meta}
            level = meta.get("level", "easy")
            # workspace/<track>/<module>/ mirrors tracks/<track>/<module>/
            module_rel = path.parent.relative_to(track["dir"])
            found[slug] = {
                "slug": slug,
                "stub": path,
                "solution": path.parent / track["solution_file"].format(slug=slug),
                "test": path.parent / track["test_file"].format(slug=slug),
                "clarify": clarify,
                "attempt": WORKSPACE / track_name / module_rel / f"{slug}{ext}",
                "track": track_name,
                "track_config": track,
                "module": path.parent.name,
                "level": level,
                "target": int(meta.get("target", TARGETS.get(level, 15))),
                "pattern": meta.get("pattern", ""),
                "kind": meta.get("kind", "write"),
            }
    return found


def get_exercise(slug: str) -> dict:
    exercises = discover()
    if slug not in exercises:
        close = [s for s in exercises if slug in s]
        hint = f" Did you mean: {', '.join(close[:5])}?" if close else ""
        die(f"No exercise called '{slug}'.{hint} See `python dojo.py list`.")
    return exercises[slug]


def find_venv_python() -> Path | None:
    for candidate in (ROOT / ".venv" / "bin" / "python",
                      ROOT / ".venv" / "Scripts" / "python.exe"):
        if candidate.exists():
            return candidate
    return None


def venv_python() -> str:
    found = find_venv_python()
    return str(found) if found else sys.executable


def run_exercise(ex: dict, target: str | None = None, quiet: bool = False) -> bool | None:
    """Run an exercise's tests with its track's test command.

    target None = the learner's attempt (or the stub if there is none yet),
    "solution" = the reference, "stub" = the blank stub.
    Returns None when the track has no test command (log those by hand).
    """
    command = ex["track_config"].get("test_command")
    if not command:
        return None
    if target == "solution":
        source = ex["solution"]
    elif target == "stub":
        source = ex["stub"]
    else:
        source = ex["attempt"] if ex["attempt"].exists() else ex["stub"]
    values = {"python": venv_python(), "test": str(ex["test"]), "source": str(source),
              "slug": ex["slug"], "root": str(ROOT), "track_dir": str(ex["track_config"]["dir"])}
    cmd = [part.format(**values) for part in command]
    env = dict(os.environ)
    env["DOJO_SOURCE"] = str(source)
    if target:
        env["DOJO_TARGET"] = target
    else:
        env.pop("DOJO_TARGET", None)
    result = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=quiet, text=True)
    return result.returncode == 0


# ------------------------------------------------------------------ log data

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
    key = d.isoformat()
    return sum(float(r["minutes"] or 0) for r in rows if r["date"] == key)


def minutes_between(rows: list[dict], start: date, end: date) -> float:
    total = 0.0
    for r in rows:
        d = parse_date(r["date"])
        if start <= d <= end:
            total += float(r["minutes"] or 0)
    return total


# --------------------------------------------------------------- spaced redo

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
    card["last"] = on.isoformat()
    card["grade"] = grade
    card["due"] = (on + timedelta(days=INTERVALS[card["box"]])).isoformat()
    reviews[item] = card
    write_json(REVIEWS, reviews)
    return card


def due_items(on: date) -> list[tuple[str, dict]]:
    reviews = read_json(REVIEWS, {})
    due = [(k, v) for k, v in reviews.items() if parse_date(v["due"]) <= on]
    return sorted(due, key=lambda kv: (kv[1]["due"], kv[1]["box"]))


# ------------------------------------------------------------------ commands

def ensure_claude_skills() -> str:
    """Make .claude/skills point at .agents/skills, the one shared copy of the skills.

    Git stores it as a symlink. A Windows checkout without symlink support turns it into a
    small text file; then try to create the link, and fall back to a copy.
    """
    import shutil
    target = ROOT / ".agents" / "skills"
    link = ROOT / ".claude" / "skills"
    if not target.is_dir():
        return "  ! .agents/skills is missing; restore it with git."
    if link.is_symlink() and link.resolve() == target.resolve():
        return "Skills: .claude/skills -> .agents/skills"
    if link.is_symlink() or link.is_file():
        link.unlink()
    elif link.is_dir():
        shutil.rmtree(link)
    link.parent.mkdir(exist_ok=True)
    try:
        link.symlink_to(Path("..") / ".agents" / "skills", target_is_directory=True)
        return "Skills: linked .claude/skills -> .agents/skills"
    except OSError:
        shutil.copytree(target, link)
        return ("Skills: copied .agents/skills to .claude/skills (no symlink support here); "
                "run `python dojo.py doctor` again after editing a skill.")


def cmd_install(args) -> None:
    """Create .venv and install requirements, the same way on every OS."""
    print(ensure_claude_skills())
    import venv
    target = ROOT / ".venv"
    if not target.exists():
        print("Creating .venv ...")
        venv.create(target, with_pip=True)
    found = find_venv_python()
    if found is None:
        die("Could not find the venv's Python. Delete .venv and try again.")
    py = str(found)
    print("Installing requirements ...")
    result = subprocess.run([py, "-m", "pip", "install", "-q", "-r", str(ROOT / "requirements.txt")])
    if result.returncode != 0:
        die("pip failed; see the messages above.")
    print("Install done.")


def cmd_export(args) -> None:
    """Zip all personal data (progress/ and workspace/), optionally copy it over SSH."""
    import zipfile
    profile = load_profile(required=False)
    target = args.to or profile.get("export_target")
    if target and (target.startswith("-") or target.startswith("rclone:-")):
        die(f"Refusing export target '{target}': a target cannot start with '-' "
            "(it would be read as an option).")
    name = re.sub(r"[^A-Za-z0-9_-]", "", profile.get("learner") or "learner") or "learner"
    out_dir = Path(args.out).expanduser() if args.out else ROOT / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"code-dojo_{name}_{now().strftime('%Y%m%d_%H%M%S')}.zip"
    count = 0
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for folder in (PROGRESS, WORKSPACE):
            if not folder.exists():
                continue
            for path in folder.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts:
                    z.write(path, path.relative_to(ROOT).as_posix())
                    count += 1
    print(f"Exported {count} files to {archive}")
    if target and target.startswith("rclone:"):
        remote = target[len("rclone:"):]
        print(f"Uploading to {remote} with rclone ...")
        if run_rclone(["copy", str(archive), remote], mounts={archive.parent: "/data"},
                      local_args={str(archive): f"/data/{archive.name}"}) != 0:
            die("rclone upload failed; the zip is still on this machine. "
                "Run `python dojo.py drive-setup` if the remote is not configured yet.")
        print("Uploaded. On the other device, download the zip, then: python dojo.py import <zip>")
    elif target:
        if shutil.which("scp") is None:
            die("scp not found. Install OpenSSH (built into Windows 10+, macOS and most Linux) "
                "or copy the zip by hand.")
        print(f"Copying to {target} ...")
        result = subprocess.run(["scp", "--", str(archive), target])
        if result.returncode != 0:
            die("scp failed; the zip is still on this machine.")
        print("Copied. On the other device: python dojo.py import <zip>")


RCLONE_IMAGE = "rclone/rclone:1.71"


def run_rclone(rclone_args: list, mounts: dict | None = None, local_args: dict | None = None,
               interactive: bool = False) -> int:
    """Run rclone from PATH, or else from its Docker image (config in ~/.config/rclone)."""
    sys.stdout.flush()
    if shutil.which("rclone"):
        return subprocess.run(["rclone", *rclone_args]).returncode
    if shutil.which("docker") is None:
        die("rclone not found. Install Docker (the rclone image is then pulled automatically) "
            "or rclone itself (https://rclone.org/install/).")
    config = Path.home() / ".config" / "rclone"
    config.mkdir(parents=True, exist_ok=True)
    cmd = ["docker", "run", "--rm", "-v", f"{config}:/config/rclone"]
    if interactive:
        cmd += ["--network", "host"]  # the Google sign-in calls back to localhost
        cmd += ["-it"] if sys.stdin.isatty() else ["-i"]
    if hasattr(os, "getuid"):
        cmd += ["--user", f"{os.getuid()}:{os.getgid()}"]
    for host_dir, container_dir in (mounts or {}).items():
        cmd += ["-v", f"{host_dir}:{container_dir}:ro"]
    args = [(local_args or {}).get(a, a) for a in rclone_args]
    return subprocess.run([*cmd, RCLONE_IMAGE, *args]).returncode


def cmd_drive_setup(args) -> None:
    """One-time Google Drive sign-in for rclone, then save the export target."""
    remote = args.remote
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", remote) or remote.startswith("-") or args.folder.startswith("-"):
        die("Remote and folder names: letters, digits, '_', '.', '-', not starting with '-'.")
    print(f"Creating the rclone remote '{remote}' for Google Drive. A sign-in link opens or is "
          "printed: log in with the Google account that should hold the exports.")
    if run_rclone(["config", "create", remote, "drive", "scope=drive.file"], interactive=True) != 0:
        die("rclone config failed.")
    target = f"rclone:{remote}:{args.folder}"
    profile = read_json(PROFILE, None)
    if profile is not None:
        profile["export_target"] = target
        write_json(PROFILE, profile)
        print(f"Saved export_target = {target}. From now on `python dojo.py export` uploads there.")
    else:
        print(f"Done. Export with: python dojo.py export --to {target}")


def cmd_import(args) -> None:
    """Restore progress/ and workspace/ from an export zip."""
    import zipfile
    archive = Path(args.archive).expanduser()
    if not archive.exists():
        die(f"No such file: {archive}")
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        bad = [n for n in names if not (n.startswith("progress/") or n.startswith("workspace/"))
               or ".." in n.replace("\\", "/").split("/") or "\\" in n or ":" in n]
        links = [i.filename for i in z.infolist() if (i.external_attr >> 16) & 0o170000 == 0o120000]
        if links:
            die(f"Refusing: the zip contains a symbolic link ({links[0]}).")
        if bad:
            die(f"Refusing: unexpected paths in the zip, e.g. {bad[0]}")
        has_data = PROFILE.exists() or LOG.exists()
        if has_data and not args.force:
            die("This copy already has progress. Run `python dojo.py export` first to keep it, "
                "then `python dojo.py import <zip> --force`.")
        if has_data:
            stamp = now().strftime("%Y%m%d_%H%M%S")
            backup = ROOT / f"progress_archive_{stamp}"
            backup.mkdir()
            for folder in (PROGRESS, WORKSPACE):
                if folder.exists():
                    shutil.move(str(folder), backup / folder.name)
            print(f"Current data moved to {backup.name}/")
        z.extractall(ROOT)
    migrate_workspace(verbose=False)  # an export from an older version may use the flat layout
    print(f"Imported {len(names)} files. Run `python dojo.py today`.")


def cmd_doctor(args) -> None:
    ok = True
    print(f"Python running dojo.py: {sys.version.split()[0]} ({sys.executable})")
    if sys.version_info < (3, 10):
        print("  ! Python 3.10 or newer is recommended.")
        ok = False
    py = venv_python()
    if find_venv_python() is None:
        print("  ! No .venv found. Create it (see README, 'Install').")
        ok = False
    check = subprocess.run([py, "-c", "import pytest; print(pytest.__version__)"],
                           capture_output=True, text=True)
    if check.returncode == 0:
        print(f"pytest: {check.stdout.strip()} ({py})")
    else:
        print("  ! pytest is not installed in the venv: pip install -r requirements.txt")
        ok = False
    profile = read_json(PROFILE, None)
    if profile:
        print(f"Profile: {profile.get('learner')}, weekly target {fmt_min(weekly_target(load_profile()))}")
    else:
        print("  ! No profile: python dojo.py setup")
        ok = False
    print(f"Exercises found: {len(discover())}")
    for name, track in load_tracks(active_only=False).items():
        reviewed = track.get("reviewed", "")
        if not reviewed:
            print(f"  note: track '{name}' has no review date (dojo-new-track, review)")
        elif (today() - parse_date(reviewed)).days > 365:
            print(f"  note: track '{name}' was last reviewed on {reviewed}: over a year ago, "
                  "worth a review against current courses and versions (dojo-new-track)")
    skills = ensure_claude_skills()
    print(skills)
    print(ensure_git_hooks())
    if skills.startswith("  !"):
        ok = False
    print("All good." if ok else "Fix the items marked ! above.")


def cmd_list(args) -> None:
    exercises = discover()
    reviews = read_json(REVIEWS, {})
    module = None
    for slug, ex in exercises.items():
        if args.module and args.module not in ex["module"]:
            continue
        if ex["module"] != module:
            module = ex["module"]
            print(f"\n{ex['track']}/{module}")
        card = reviews.get(slug)
        if not card:
            status = "new"
        elif card["box"] >= MASTERED_BOX:
            status = "mastered"
        else:
            status = f"box {card['box']}, due {card['due']}"
        print(f"  {slug:28} {ex['level']:6} {ex['target']:>3}m  {status}")


def cmd_start(args) -> None:
    ensure_files()
    timers = read_json(TIMER, {})
    if args.item in timers:
        die(f"'{args.item}' is already running since {timer_of(timers[args.item])['start']}.")
    ex = discover().get(args.item)
    if ex:
        due = [k for k, _ in due_items(today()) if k != args.item]
        if args.item not in read_json(REVIEWS, {}) and due:
            print(f"Reminder: {len(due)} redo(s) due ({', '.join(due[:4])}). "
                  "Best practice: clear the redo queue before new material.")
        attempt = ex["attempt"]
        attempt.parent.mkdir(parents=True, exist_ok=True)
        shown = attempt.relative_to(ROOT).as_posix()
        card = read_json(REVIEWS, {}).get(args.item)
        redo = card is not None and card.get("grade") != "failed"
        if attempt.exists() and (args.fresh or redo):
            history = attempt.parent / HISTORY_DIR
            history.mkdir(parents=True, exist_ok=True)
            stamp = now().strftime("%Y%m%d_%H%M")
            shutil.move(str(attempt), history / f"{args.item}_{stamp}{attempt.suffix}")
        if not attempt.exists():
            shutil.copy(ex["stub"], attempt)
            print(f"Fresh file: {shown}")
            if redo:
                print(f"Redo from a blank file: do not open {HISTORY_DIR}/ or old notes.")
        else:
            print(f"Continuing your file: {shown}")
        print(f"Target: {ex['target']} min ({ex['level']}). "
              f"Test with: python dojo.py test {args.item}")
        print(CHECKLIST)
    else:
        print(f"Timer started for '{args.item}' (not a dojo exercise; log it with `done` as usual).")
    timers[args.item] = {"start": now().isoformat(), "paused_total": 0.0, "paused_at": None}
    write_json(TIMER, timers)


def cmd_test(args) -> None:
    ex = get_exercise(args.item)
    target = "solution" if args.solution else None
    if target is None:
        warn_if_unsaved(ex)
    if args.debug:
        sys.exit(debug_in_process(ex, target))
    passed = run_exercise(ex, target=target)
    if passed is None:
        die(f"Track '{ex['track']}' has no test command; check your work with the tutor.")
    sys.exit(0 if passed else 1)


def warn_if_unsaved(ex: dict) -> None:
    """Warn when the attempt is still byte-for-byte the stub: usually an unsaved editor buffer."""
    attempt, stub = ex["attempt"], ex["stub"]
    try:
        unchanged = attempt.read_bytes() == stub.read_bytes()
    except OSError:
        return
    if unchanged:
        print(f"Warning: {attempt.relative_to(ROOT).as_posix()} is unchanged from the stub. "
              "Did you save the file?", file=sys.stderr)


def debug_in_process(ex: dict, target: str | None) -> int:
    """Run a pytest-based exercise inside this process so editor breakpoints work.

    The editor's debugger must start dojo.py with the venv's Python (VS Code and Zed
    pick .venv automatically).
    """
    command = ex["track_config"].get("test_command") or []
    if not any("pytest" in part for part in command):
        die("--debug works for pytest-based tracks; debug other tracks with their own tools.")
    try:
        import pytest
    except ImportError:
        die("pytest is not importable here: start the debugger with the .venv interpreter.")
    if target:
        os.environ["DOJO_TARGET"] = target
    else:
        os.environ.pop("DOJO_TARGET", None)
    os.chdir(ROOT)
    return pytest.main(["-q", "--no-header", "-p", "no:cacheprovider", str(ex["test"])])


def cmd_done(args) -> None:
    ensure_files()
    timers = read_json(TIMER, {})
    started = timers.pop(args.item, None)
    if args.minutes is not None:
        minutes = float(args.minutes)
    elif started:
        minutes = timer_minutes(started)
    else:
        die("No timer running for this item. Pass --minutes N.")
    write_json(TIMER, timers)
    credit = max(0.0, min(float(args.credit or 0), minutes))
    minutes -= credit
    on = parse_date(args.date) if args.date else today()
    paused = paused_minutes(started) if started and args.minutes is None else 0.0

    if args.item.startswith(LESSON_PREFIX):
        # A PRIMM lesson: training time, but no target, no tests and no redo schedule.
        topic = args.item[len(LESSON_PREFIX):]
        module = timer_of(started).get("module", "") if started else ""
        append_log({"date": on.isoformat(), "item": topic, "kind": "study", "module": module,
                    "minutes": round(minutes + credit + paused, 1), "note": "PRIMM lesson"})
        print(f"Lesson '{topic}': {fmt_min(minutes + credit + paused)} logged as study.")
        return

    ex = discover().get(args.item)
    if ex:
        passed = run_exercise(ex, quiet=True)
        if passed is None:
            passed = args.result != "failed"
        kind, module, pattern, level, target = "exercise", ex["module"], ex["pattern"], ex["level"], ex["target"]
    else:
        passed = args.result not in ("failed", "fail")
        kind = args.kind or "external"
        module, pattern, level = args.module or "", args.pattern or "", args.level or ""
        target = args.target or TARGETS.get(level, 0)

    if args.gave_up:
        result = "gave_up"
    elif args.result in ("strong", "pass", "fail"):
        result = args.result
    elif passed:
        result = "solved"
    else:
        result = "failed"
    ratio = round(minutes / target, 2) if target else None
    skipped = [x.strip().lower() for x in (args.skipped or "").split(",") if x.strip()]
    unknown = [x for x in skipped if x not in STEPS]
    if unknown:
        die(f"Unknown step(s): {', '.join(unknown)}. Steps: {', '.join(STEPS)}")
    append_log({"date": on.isoformat(), "item": args.item, "kind": kind, "module": module,
                "pattern": pattern, "level": level, "minutes": round(minutes, 1),
                "target": target or "", "hints": args.hints, "result": result,
                "ratio": ratio if ratio is not None else "",
                "skipped": ",".join(skipped), "note": args.note or ""})
    if credit:
        # Time lost to a tutor misunderstanding: off the solve time, still counted as training.
        append_log({"date": on.isoformat(), "item": args.item, "kind": "study",
                    "minutes": round(credit, 1), "note": "credit: tutor misunderstanding"})
    if paused >= 0.5:
        # Clock paused for a discussion: off the solve time, still counted as training.
        append_log({"date": on.isoformat(), "item": args.item, "kind": "study",
                    "minutes": round(paused, 1), "note": "paused: discussion"})

    verdict = f"{args.item}: {result} in {fmt_min(minutes)}"
    if ratio is not None:
        verdict += f" ({ratio}x target {target}m)"
    verdict += f", hints {args.hints}."
    if credit:
        verdict += f" ({fmt_min(credit)} credited back.)"
    if paused >= 0.5:
        verdict += f" ({fmt_min(paused)} paused, logged as study.)"
    print(verdict)
    if ex and ex["pattern"]:
        print(f"Pattern: {ex['pattern']}")
    if ratio is not None and ratio > 2 and args.hints == 0 and result != "solved":
        print("Over twice the target without a hint: next time ask for hint 1 at 2x; "
              "an hour of struggle teaches less than a hint and a redo tomorrow.")
    elif ratio is not None and ratio > 2 and args.hints == 0:
        print("Solved, but over twice the target without a hint: next time ask for hint 1 at 2x.")
    if skipped:
        print(f"Process: skipped {', '.join(skipped)}. Next time do every step; it is the habit "
              "the interview tests.")
    if ex and result == "failed":
        print("Tests do not pass yet. Keep going (`start` again) or add --gave-up.")
    if kind in ("exercise", "external") and not args.no_review:
        card = schedule(args.item, result, ratio, args.hints, on)
        label = {"clean": "Clean solve.", "ok": "Solid.", "struggled": "Struggled: redo soon.",
                 "failed": "Not solved: redo tomorrow."}[card["grade"]]
        print(f"{label} Next redo from a blank file: {card['due']} (box {card['box']}).")


def cmd_log(args) -> None:
    ensure_files()
    on = parse_date(args.date) if args.date else today()
    append_log({"date": on.isoformat(), "item": args.item or args.kind, "kind": args.kind,
                "minutes": args.minutes, "hints": args.hints, "result": args.result or "",
                "pattern": args.pattern or "", "level": args.level or "", "note": args.note or ""})
    print(f"Logged {fmt_min(args.minutes)} of {args.kind} on {on}.")


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


def cmd_pause(args) -> None:
    """Stop the clock while talking things through (a concept, a long hint)."""
    timers = read_json(TIMER, {})
    item = pick_timer(timers, args.item)
    t = timer_of(timers[item])
    if t["paused_at"]:
        die(f"'{item}' is already paused.")
    t["paused_at"] = now().isoformat()
    timers[item] = t
    write_json(TIMER, timers)
    print(f"Paused '{item}' at {fmt_min(timer_minutes(t))}. Resume with: python dojo.py resume")


def cmd_resume(args) -> None:
    timers = read_json(TIMER, {})
    item = pick_timer(timers, args.item)
    t = timer_of(timers[item])
    if not t["paused_at"]:
        die(f"'{item}' is not paused.")
    t["paused_total"] += (now() - datetime.fromisoformat(t["paused_at"])).total_seconds()
    t["paused_at"] = None
    timers[item] = t
    write_json(TIMER, timers)
    print(f"Resumed '{item}' ({fmt_min(timer_minutes(t))} so far).")


def cmd_clarify(args) -> None:
    """Show the interviewer's answers to clarifying questions (after listing your own)."""
    ex = get_exercise(args.item)
    if not ex["clarify"].exists():
        die("No clarifications for this exercise: the task text is the full specification.")
    lines = [l for l in ex["clarify"].read_text(encoding="utf-8").splitlines()
             if not l.startswith("Pattern:")]
    print(re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip())


def cmd_cancel(args) -> None:
    timers = read_json(TIMER, {})
    if timers.pop(args.item, None) is None:
        die(f"No timer for '{args.item}'.")
    write_json(TIMER, timers)
    print(f"Timer for '{args.item}' cancelled.")


def cmd_mark(args) -> None:
    """Seed the redo schedule for work already known (used by placement)."""
    ensure_files()
    exercises = discover()
    slugs = [s for s, ex in exercises.items()
             if s in args.items or any(ex["module"].startswith(i) for i in args.items)]
    unknown = [i for i in args.items if i not in exercises
               and not any(ex["module"].startswith(i) for ex in exercises.values())]
    if unknown:
        die("Unknown exercise or module: " + ", ".join(unknown))
    reviews = read_json(REVIEWS, {})
    on = today()
    box = max(0, min(args.box, len(INTERVALS) - 1))
    for slug in slugs:
        card = reviews.get(slug, {"box": 0, "attempts": 0, "clean": 0})
        card.update({"box": box, "grade": "placed", "last": on.isoformat(),
                     "due": (on + timedelta(days=INTERVALS[box])).isoformat()})
        reviews[slug] = card
    write_json(REVIEWS, reviews)
    print(f"Placed {len(slugs)} exercises in box {box} (first redo in {INTERVALS[box]} days).")


def cmd_mistake(args) -> None:
    ensure_files()
    clean = [s.replace("|", "/").replace("\n", " ") for s in (args.item, args.what, args.fix)]
    with MISTAKES.open("a", encoding="utf-8") as f:
        f.write(f"| {today().isoformat()} | {clean[0]} | {clean[1]} | {clean[2]} |\n")
    print("Mistake logged.")


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


def exercise_hash(ex: dict) -> str:
    """What the learner sees and is tested on: task, tests and clarify answers."""
    h = hashlib.sha256()
    for path in (ex["stub"], ex["test"], ex["clarify"]):
        h.update(path.read_bytes() if path.exists() else b"")
    return h.hexdigest()[:16]


TOPICS_RE = re.compile(r"can cover:\s*(.+?)\.?\s*$", re.MULTILINE)


def module_topics() -> dict:
    """track/module -> the lesson topics its primm/README.md lists."""
    out = {}
    for track_name, track in load_tracks(active_only=True).items():
        for readme in sorted(track["dir"].glob(f"*/{PRIMM_DIR}/README.md")):
            m = TOPICS_RE.search(readme.read_text(encoding="utf-8"))
            if m:
                out[f"{track_name}/{readme.parent.parent.name}"] = [t.strip() for t in m.group(1).split(", ") if t.strip()]
    return out


def skipped_module(module: str, profile: dict) -> bool:
    return any(module.split("/")[-1].startswith(x) for x in profile.get("skip_modules", []))


def started_modules() -> set[str]:
    """Modules with at least one attempted exercise: the only ones whose changes need a question.
    New material in a module the learner has not reached yet simply waits for them there."""
    reviews = read_json(REVIEWS, {})
    return {ex["module"] for slug, ex in discover().items() if slug in reviews}


def topic_changes() -> dict:
    """New lesson topics per module since the learner was last asked (modules they skip stay quiet)."""
    current = module_topics()
    if not TOPICS_SEEN.exists():
        if PROFILE.exists():
            write_json(TOPICS_SEEN, current)
        return {}
    seen = read_json(TOPICS_SEEN, {})
    profile = read_json(PROFILE, {})
    started = started_modules()
    out = {}
    for module in sorted(set(current) | set(seen)):
        if skipped_module(module, profile) or module.split("/")[-1] not in started:
            if module in current and seen.get(module) != current[module]:
                seen[module] = current[module]  # recorded silently: met when the module is reached
                write_json(TOPICS_SEEN, seen)
            continue
        new = [t for t in current.get(module, []) if t not in seen.get(module, [])]
        gone = [t for t in seen.get(module, []) if t not in current.get(module, [])]
        # "default arguments" -> "default and keyword arguments" is a rewording, not a removal
        reworded = [(g, n) for g in gone for n in new
                    if all(w in n.lower() for w in g.lower().split())]
        new = [n for n in new if n not in {r[1] for r in reworded}] + \
              [f"{n} (was: {g})" for g, n in reworded if n != g and any(w not in g.lower() for w in n.lower().split())]
        gone = [g for g in gone if g not in {r[0] for r in reworded}]
        if new or gone:
            out[module] = {"new": new, "removed": gone}
    return out


def track_changes() -> dict:
    """New, changed and removed exercises in the learner's tracks since they were last asked.
    The first run records everything as seen, so a new learner is not asked about every exercise."""
    current = {slug: exercise_hash(ex) for slug, ex in discover().items()}
    if not SEEN.exists():
        if PROFILE.exists():
            write_json(SEEN, current)
        return {"new": [], "changed": [], "removed": [], "topics": topic_changes()}
    seen = read_json(SEEN, {})
    profile = read_json(PROFILE, {})
    exercises = discover()
    started = started_modules()
    quiet = {sl for sl, ex in exercises.items()
             if skipped_module(ex["module"], profile) or ex["module"] not in started}
    silent = {sl: current[sl] for sl in quiet if seen.get(sl) != current[sl]}
    if silent:  # nothing to ask: new material in an unreached module is met there
        seen.update(silent)
        write_json(SEEN, seen)
    return {"new": [s for s in current if s not in seen and s not in quiet],
            "changed": [s for s in current if s in seen and seen[s] != current[s] and s not in quiet],
            "removed": [s for s in seen if s not in current],
            "topics": topic_changes()}


def acknowledge_changes(slugs: list[str] | None = None) -> None:
    current = {slug: exercise_hash(ex) for slug, ex in discover().items()}
    seen = read_json(SEEN, {})
    reviews = read_json(REVIEWS, {})
    for slug in (slugs or list(current) + list(seen)):
        if slug in current:
            seen[slug] = current[slug]
        else:
            seen.pop(slug, None)
            reviews.pop(slug, None)  # the exercise is gone; its history stays in the log
    write_json(SEEN, seen)
    write_json(REVIEWS, reviews)
    if not slugs:  # acknowledging everything includes the lesson topics
        write_json(TOPICS_SEEN, module_topics())


def changes_lines(changes: dict) -> list[str]:
    exercises = discover()
    lines = []
    topics = changes.get("topics", {})
    for kind in ("new", "removed"):
        parts = [f"{m} ({', '.join(t[kind])})" for m, t in topics.items() if t[kind]]
        if parts:
            lines.append(f"{kind} lesson topics: " + "; ".join(parts))
    for kind in ("new", "changed", "removed"):
        if not changes[kind]:
            continue
        if kind == "removed":
            lines.append(f"{len(changes[kind])} removed exercise(s): {', '.join(changes[kind])} "
                         "(recording them as seen drops them from your redo schedule)")
            continue
        by_module: dict[str, list[str]] = {}
        for slug in changes[kind]:
            module = f"{exercises[slug]['track']}/{exercises[slug]['module']}" if slug in exercises else "?"
            by_module.setdefault(module, []).append(slug)
        lines.append(f"{len(changes[kind])} {kind}: " + "; ".join(
            f"{m} ({', '.join(sl)})" for m, sl in by_module.items()))
    return lines


def upstream_remote() -> str:
    names = subprocess.run(["git", "-C", str(ROOT), "remote"], capture_output=True, text=True).stdout.split()
    return "upstream" if "upstream" in names else ("origin" if "origin" in names else "")


def upstream_behind(fetch: bool) -> int | None:
    """Commits on the shared repo's main branch that this copy does not have (None = unknown)."""
    remote = upstream_remote()
    if not remote:
        return None
    if fetch:
        try:
            subprocess.run(["git", "-C", str(ROOT), "fetch", "--quiet", remote],
                           capture_output=True, timeout=8)
        except (subprocess.TimeoutExpired, OSError):
            return None
    branch = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--abbrev-ref", f"{remote}/HEAD"],
                            capture_output=True, text=True).stdout.strip() or f"{remote}/main"
    out = subprocess.run(["git", "-C", str(ROOT), "rev-list", "--count", f"HEAD..{branch}"],
                         capture_output=True, text=True)
    return int(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip().isdigit() else None


def daily_upstream_check() -> int | None:
    """At most one network check a day, so session start stays fast."""
    state = read_json(UPSTREAM_CHECK, {})
    if state.get("date") == today().isoformat():
        return state.get("behind")
    behind = upstream_behind(fetch=True)
    if PROGRESS.exists():
        write_json(UPSTREAM_CHECK, {"date": today().isoformat(), "behind": behind})
    return behind


def cmd_changes(args) -> None:
    """Show track changes since the learner was last asked; --ack records them as seen."""
    load_profile()
    if args.ack is not None:
        acknowledge_changes(args.ack or None)
        print("Recorded as seen" + (f": {', '.join(args.ack)}." if args.ack else ": all current changes."))
        return
    lines = changes_lines(track_changes())
    if not lines:
        print("No track changes since you were last asked.")
        return
    print("Track changes since you were last asked:")
    for line in lines:
        print("  " + line)
    print("For each new or changed exercise: learn it (nothing to do), already know it "
          "(`mark <slug> --box 3`), or not for me (`settings skip_exercises+=<slug>`, or skip_modules+=<module>).")
    print("For a changed exercise: redo the new version (nothing to do), already know it "
          "(`mark <slug> --box 3`), or leave it out (`settings skip_exercises+=<slug>`).")
    print("For new lesson topics: learn it (`teach me <topic>`, now or when that module comes up), "
          "already know it, or not for me. Removed exercises and topics: tell the learner, then acknowledge.")
    print("Then: python dojo.py changes --ack [slugs]")


def cmd_update(args) -> None:
    """Pull the shared repo's latest tracks and docs, then show what changed in your tracks."""
    remote = upstream_remote()
    if not remote:
        die("No git remote found: this copy cannot be updated with git.")
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=no"],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        die("You have local changes to shared files (git status shows them). Commit or stash them, "
            "then run update again.")
    branch = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "-C", str(ROOT), "fetch", "--quiet", remote, branch])
    incoming = f"HEAD..{remote}/{branch}"
    log = subprocess.run(["git", "-C", str(ROOT), "log", "--oneline", incoming],
                         capture_output=True, text=True).stdout.strip()
    if not log:
        print("Already up to date.")
        write_json(UPSTREAM_CHECK, {"date": today().isoformat(), "behind": 0})
        cmd_changes(argparse.Namespace(ack=None))
        return
    files = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", incoming],
                           capture_output=True, text=True).stdout.split()
    runs = [f for f in files if f.endswith((".py", ".sh", "track.json")) or f.startswith((".claude/", ".githooks/", ".github/"))]
    print(f"Incoming from {remote}/{branch}:\n" + "\n".join("  " + line for line in log.splitlines()))
    print(f"{len(files)} file(s) change" + (f"; these run on your machine, so they are worth a look "
          f"(git diff {incoming} -- <file>):\n  " + "\n  ".join(runs) if runs else "."))
    if not args.yes:
        if not sys.stdin.isatty():
            die("Run `python dojo.py update --yes` to apply them.")
        if not ask("Apply them? (y/n)", "y").lower().startswith("y"):
            print("Nothing changed.")
            return
    result = subprocess.run(["git", "-C", str(ROOT), "merge", "--ff-only", f"{remote}/{branch}"])
    if result.returncode != 0:
        die("The update could not be applied automatically (see the git message above).")
    write_json(UPSTREAM_CHECK, {"date": today().isoformat(), "behind": 0})
    cmd_changes(argparse.Namespace(ack=None))


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


def cmd_modules(args) -> None:
    """Show the learner's modules; the tutor goes through them with the learner (dojo-assess)."""
    print_modules(load_profile())
    print("Leave one out: python dojo.py settings skip_modules+=<module>; add one back: skip_modules-=<module>.")


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


def cmd_mix(args) -> None:
    """Show or set the share of new-material time per track, and the current priority."""
    profile = load_profile()
    available = load_tracks(active_only=False)
    mix = effective_mix(profile)
    if args.shares:
        for share in args.shares:
            name, _, value = share.partition("=")
            if name not in available or not value.isdigit():
                die(f"Use track=percent with one of: {', '.join(available)} (got '{share}').")
            mix[name] = int(value)
            if name not in profile["tracks"]:
                profile["tracks"] = list(profile["tracks"] or load_tracks(active_only=True)) + [name]
        if sum(mix.values()) != 100:
            die("The shares must add up to 100 (0 = maintenance). Would be: "
                + ", ".join(f"{t}={v}" for t, v in mix.items()))
        profile["mix"] = mix
    if args.priority is not None:
        profile["priority"] = args.priority
    if args.shares or args.priority is not None:
        write_json(PROFILE, profile)
        print("Saved. Record the reason under 'Plan changes' in progress/PLAN.md.")
    for name, value in mix.items():
        state = "maintenance (redos only)" if value == 0 else f"{value}% of new material"
        print(f"  {name:12} {state}")
        if args.shares and value > 0 and available[name]["requires"]:
            print("    requires: " + "; ".join(available[name]["requires"]))
    print(f"Priority: {profile.get('priority') or '(none)'}")


def cmd_today(args, brief: bool = False) -> None:
    profile = load_profile(required=not brief)
    if not PROFILE.exists():
        print("[dojo] New learner, no profile yet: offer to set them up in chat (dojo-assess, step 0),\n"
              "or they run `python dojo.py setup` in a terminal.")
        return
    rows = read_log()
    on = today()
    plan = planned_minutes(profile, on)
    done_today = minutes_on(rows, on)
    wk = week_numbers(profile, rows, on)
    due = due_items(on)
    timers = read_json(TIMER, {})
    mix = effective_mix(profile)
    upcoming = next_new(profile)

    lines = []
    day_name = on.strftime("%A %d %B %Y")
    lines.append(f"{day_name}: {fmt_min(done_today)} of {fmt_min(plan)} planned today"
                 + (" (rest day)" if plan == 0 else "") + ".")
    gap = wk["gap"]
    status = "on track" if gap >= -15 else f"behind by {fmt_min(-gap)}"
    if gap > 15:
        status = f"ahead by {fmt_min(gap)}"
    lines.append(f"This week: {fmt_min(wk['done'])} of {fmt_min(wk['target'])} ({status}).")
    if gap < -15 and wk["remaining_days"]:
        days = wk["remaining_days"]
        extra = min(-gap / len(days), 60)
        names = ", ".join("today" if d == on else d.strftime("%A") for d in days)
        line = f"  Catch-up: add about {fmt_min(extra)} on each of: {names}"
        if profile["flexible_rest_day"]:
            line += " (or train on the rest day)"
        left = -gap - extra * len(days)
        if left > 15:
            line += (f". About {fmt_min(left)} will stay open this week: let it go, "
                     "it does not carry over.")
        lines.append(line + ("" if left > 15 else "."))
    if wk["prev_gap"] < -60 and on.weekday() < 2:
        lines.append(f"  Last week finished {fmt_min(-wk['prev_gap'])} short. Do not try to repay it all; "
                     "prioritise the redo queue this week.")
    if profile.get("target_date"):
        days_left = (parse_date(profile["target_date"]) - on).days
        if days_left >= 0:
            lines.append(f"Target date {profile['target_date']}: {days_left} days left.")
    if timers:
        lines.append("Timers running: " + ", ".join(
            f"{k} ({fmt_min(timer_minutes(v))} so far{', PAUSED' if timer_of(v)['paused_at'] else ''})"
            for k, v in timers.items()))
    if due:
        names = ", ".join(f"{k} (box {v['box']})" for k, v in due[:8])
        more = f" and {len(due) - 8} more" if len(due) > 8 else ""
        lines.append(f"Redo queue ({len(due)} due): {names}{more}.")
    else:
        lines.append("Redo queue: nothing due.")
    if profile.get("mode") or profile.get("target_level"):
        lines.append("Mode: " + (profile.get("mode") or "not set")
                     + ", target level: " + (profile.get("target_level") or "not set") + ".")
    if profile.get("priority"):
        lines.append(f"Priority: {profile['priority']}.")
    if len(mix) > 1:
        lines.append("Mix: " + ", ".join(
            f"{t} maintenance (redos only)" if v == 0
            else f"{t} {v}%" + (f" (about {fmt_min(plan * v / 100)} of today)" if plan else "")
            for t, v in mix.items()) + ".")
        for t, v in mix.items():
            items = next_new(profile, track=t) if v > 0 else []
            if items:
                lines.append(f"Next new ({t}): " + ", ".join(f"{e['slug']} ({e['module']})" for e in items) + ".")
    elif upcoming:
        lines.append("Next new: " + ", ".join(f"{e['slug']} ({e['module']})" for e in upcoming) + ".")
    weak = [(p, s) for p, s in recent_stats(rows, 14, on).items()
            if s["n"] >= 2 and (s["ratio"] > 1.5 or s["hints"] > 1.5)]
    if weak:
        lines.append("Weak spots (last 14 days): " + ", ".join(
            f"{p} ({s['ratio']:.1f}x, {s['hints']:.1f} hints)" for p, s in weak[:5]) + ".")
    changes = changes_lines(track_changes())
    if changes:
        lines.append("Track changes to ask about (learn it / already know it / not for me): "
                     + " | ".join(changes) + ". Details: `python dojo.py changes`.")
    behind = daily_upstream_check() if brief else upstream_behind(fetch=False)
    if behind:
        lines.append(f"Updates on the shared repo: {behind} new commit(s). Say `update` "
                     "or run `python dojo.py update`.")
    if brief:
        print("[dojo status, from `python dojo.py brief`]")
    print("\n".join(lines))
    if not brief:
        print("\nSession plan for today: see docs/DAILY_SESSION.md "
              f"(the {session_size(plan)} version).")


def session_size(minutes: int) -> str:
    if minutes >= 150:
        return "full (3h)"
    if minutes >= 90:
        return "standard (2h)"
    if minutes >= 45:
        return "short (1h)"
    return "minimum (30m)"


def cmd_week(args) -> None:
    profile = load_profile()
    rows = read_log()
    on = parse_date(args.date) if args.date else today()
    start = week_start(on)
    end = start + timedelta(days=6)
    wk_rows = [r for r in rows if start <= parse_date(r["date"]) <= end]
    total = sum(float(r["minutes"] or 0) for r in wk_rows)
    target = weekly_target(profile)
    by_kind: dict[str, float] = {}
    for r in wk_rows:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + float(r["minutes"] or 0)
    per_day = [(start + timedelta(days=i)) for i in range(7)]
    stats = recent_stats(rows, (on - start).days + 1, on)
    attempts = [r for r in wk_rows if r["kind"] in ("exercise", "external")]
    solved = [r for r in attempts if r["result"] == "solved"]
    clean = [r for r in solved if int(r["hints"] or 0) == 0 and r["ratio"] and float(r["ratio"]) <= 1.0]
    reviews = read_json(REVIEWS, {})
    mastered = sum(1 for c in reviews.values() if c["box"] >= MASTERED_BOX)
    mistakes = [line for line in (MISTAKES.read_text(encoding="utf-8").splitlines() if MISTAKES.exists() else [])
                if line.startswith("| 2") and start.isoformat() <= line[2:12] <= end.isoformat()]

    iso = on.isocalendar()
    out = [f"# Week {iso[0]}-W{iso[1]:02d} ({start} to {end})", ""]
    pct = 100 * total / target if target else 0
    out.append(f"**Time:** {fmt_min(total)} of {fmt_min(target)} ({pct:.0f}%).")
    out.append("")
    out.append("| Day | Planned | Done |")
    out.append("| --- | --- | --- |")
    for d in per_day:
        out.append(f"| {d.strftime('%a %d')} | {fmt_min(planned_minutes(profile, d))} | {fmt_min(minutes_on(rows, d))} |")
    out.append("")
    out.append("**By activity:** " + (", ".join(f"{k} {fmt_min(v)}" for k, v in sorted(by_kind.items())) or "none"))
    out.append("")
    out.append(f"**Problems:** {len(attempts)} attempted, {len(solved)} solved, "
               f"{len(clean)} clean (no hints, within target). Mastered items overall: {mastered}.")
    out.append("")
    if stats:
        out.append("| Pattern | Attempts | Median time ratio | Avg hints | Clean |")
        out.append("| --- | --- | --- | --- | --- |")
        for p, s in sorted(stats.items(), key=lambda kv: -kv[1]["ratio"]):
            out.append(f"| {p} | {s['n']} | {s['ratio']:.2f}x | {s['hints']:.1f} | {s['clean']} |")
        out.append("")
    tracked = [r for r in attempts if "skipped" in r]
    if tracked:
        full = sum(1 for r in tracked if not r.get("skipped"))
        counts: dict[str, int] = {}
        for r in tracked:
            for step in filter(None, (r.get("skipped") or "").split(",")):
                counts[step] = counts.get(step, 0) + 1
        line = f"**Process:** every step followed in {full} of {len(tracked)} attempts ({100 * full / len(tracked):.0f}%)."
        if counts:
            line += " Most skipped: " + ", ".join(f"{k} ({v})" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])) + "."
        out.append(line)
        out.append("")
    out.append(f"**Mistakes logged:** {len(mistakes)}")
    out.extend(mistakes)
    out.append("")
    out.append("## Coach notes")
    out.append("")
    out.append("_Filled in by the tutor during the weekly review (`/dojo-weekly`)._")
    text = "\n".join(out) + "\n"
    print(text)
    if args.write:
        WEEKLY.mkdir(parents=True, exist_ok=True)
        path = WEEKLY / f"{iso[0]}-W{iso[1]:02d}.md"
        if path.exists() and not args.force:
            print(f"{path.relative_to(ROOT)} exists; pass --force to overwrite.")
        else:
            path.write_text(text, encoding="utf-8")
            print(f"Written to {path.relative_to(ROOT)}")


def cmd_stats(args) -> None:
    rows = read_log()
    on = today()
    exercises = discover()
    reviews = read_json(REVIEWS, {})
    total = sum(float(r["minutes"] or 0) for r in rows)
    print(f"Total logged: {fmt_min(total)} over {len({r['date'] for r in rows})} days.\n")
    print("Modules (exercises tried / total, mastered):")
    modules: dict[str, list[str]] = {}
    for slug, ex in exercises.items():
        modules.setdefault(f"{ex['track']}/{ex['module']}", []).append(slug)
    for name, slugs in modules.items():
        tried = sum(1 for s in slugs if s in reviews)
        mastered = sum(1 for s in slugs if reviews.get(s, {}).get("box", 0) >= MASTERED_BOX)
        print(f"  {name:40} {tried:>2}/{len(slugs):<2} mastered {mastered}")
    mix = effective_mix(load_profile(required=False))
    if len(mix) > 1:
        module_track = {ex["module"]: ex["track"] for ex in exercises.values()}
        since = on - timedelta(days=28)
        spent: dict[str, float] = {}
        for r in rows:
            if parse_date(r["date"]) > since and r["module"] in module_track:
                t = module_track[r["module"]]
                spent[t] = spent.get(t, 0.0) + float(r["minutes"] or 0)
        total_t = sum(spent.values()) or 1
        print("Track time, last 28 days (exercises and lessons with a module) against the mix:")
        for t, v in mix.items():
            print(f"  {t:12} {fmt_min(spent.get(t, 0))} ({100 * spent.get(t, 0) / total_t:.0f}%), mix {v}%")
        print()
    print("\nLast 28 days by pattern:")
    for p, s in sorted(recent_stats(rows, 28, on).items(), key=lambda kv: -kv[1]["ratio"]):
        print(f"  {p:28} n={s['n']:<3} median {s['ratio']:.2f}x  hints {s['hints']:.1f}  clean {s['clean']}")
    print("\nFluency gates (see the track README, section 'Milestones'):")
    for label, check in fluency_gates(rows, on):
        print(f"  [{'x' if check else ' '}] {label}")


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


def cmd_sync(args) -> None:
    """Find workspace files changed since they were last logged."""
    ensure_files()
    rows = read_log()
    last_logged: dict[str, datetime] = {}
    for r in rows:
        last_logged[r["item"]] = datetime.fromisoformat(r["date"] + "T23:59:59")
    timers = read_json(TIMER, {})
    exercises = discover()
    found = False
    for slug, ex in exercises.items():
        path = ex["attempt"]
        if not path.exists() or slug in timers:
            continue
        changed = datetime.fromtimestamp(path.stat().st_mtime)
        if slug not in last_logged or changed > last_logged[slug]:
            passed = run_exercise(exercises[slug], quiet=True)
            state = {True: "passes", False: "does not pass", None: "no test command"}[passed]
            print(f"  {slug}: edited {changed:%Y-%m-%d %H:%M}, not logged, tests {state}.")
            found = True
    for item, started in timers.items():
        print(f"  Timer still running: {item} since {timer_of(started)['start']}.")
        found = True
    if not found:
        print("Everything is logged.")
    else:
        print("Log untimed work with: python dojo.py done <item> --minutes N --hints H")


def cmd_verify(args) -> None:
    """For maintainers: every stub must fail and every reference solution must pass."""
    exercises = discover()
    if args.items:
        exercises = {k: v for k, v in exercises.items() if k in args.items}
    bad = []
    for slug, ex in exercises.items():
        if not ex["track_config"].get("test_command"):
            continue
        if not ex["test"].exists() or not ex["solution"].exists():
            bad.append(f"{slug}: missing test or solution file")
            continue
        if not run_exercise(ex, target="solution", quiet=True):
            bad.append(f"{slug}: reference solution FAILS its tests")
        if run_exercise(ex, target="stub", quiet=True):
            bad.append(f"{slug}: stub PASSES its tests (tests too weak)")
    print(f"Checked {len(exercises)} exercises.")
    for line in bad:
        print("  " + line)
    sys.exit(1 if bad else 0)


def modules_by_name() -> dict:
    """Map module folder name -> (track name, module path relative to the track, track settings)."""
    found = {}
    for ex in discover().values():
        rel = ex["stub"].parent.relative_to(ex["track_config"]["dir"])
        found.setdefault(ex["module"], (ex["track"], rel, ex["track_config"]))
    return found


def cmd_primm(args) -> None:
    """Create (or show) the PRIMM folder of a module in the workspace, and optionally a lesson file."""
    modules = modules_by_name()
    matches = [m for m in modules if args.module == m] or [m for m in modules if args.module in m]
    if len(matches) != 1:
        hint = ", ".join(matches) if matches else ", ".join(modules)
        die(f"Which module? {hint}")
    track_name, rel, track = modules[matches[0]]
    folder = WORKSPACE / track_name / rel / PRIMM_DIR
    folder.mkdir(parents=True, exist_ok=True)
    print(f"PRIMM folder: {folder.relative_to(ROOT).as_posix()}/")
    if args.topic:
        topic = re.sub(r"[^a-z0-9_]+", "_", args.topic.lower()).strip("_") or "lesson"
        lesson = folder / f"{topic}{track['extension']}"
        if not lesson.exists():
            lesson.touch()
            print(f"Lesson file (empty, you type it): {lesson.relative_to(ROOT).as_posix()}")
        else:
            print(f"Lesson file already there: {lesson.relative_to(ROOT).as_posix()}")
        key = f"{LESSON_PREFIX}{topic}"
        timers = read_json(TIMER, {})
        if key in timers:
            print(f"Lesson timer already running since {timer_of(timers[key])['start']}.")
        else:
            timers[key] = {"start": now().isoformat(), "paused_total": 0.0, "paused_at": None,
                           "module": matches[0]}
            write_json(TIMER, timers)
            print(f"Lesson timer started. End it with: python dojo.py done {key}")


HISTORY_STAMP_RE = re.compile(r"^(?P<slug>[a-z0-9_]+?)_\d{8}_\d{4}(?P<ext>\.[A-Za-z0-9]+)$")


def migrate_workspace(verbose: bool = True) -> int:
    """Move files from the old flat layout into workspace/<track>/<module>/. Idempotent.

    Old layout: workspace/<track>/<slug>.<ext> and workspace/.history/<slug>_<stamp>.<ext>.
    Loose files that are not exercises go to workspace/<track>/scratch/. Nothing is
    overwritten: a name clash is reported and left in place.
    """
    if not WORKSPACE.exists():
        return 0
    exercises = discover(active_only=False)
    moves = []
    for track_name in load_tracks(active_only=False):
        folder = WORKSPACE / track_name
        if not folder.is_dir():
            continue
        for path in sorted(p for p in folder.iterdir() if p.is_file()):
            ex = exercises.get(path.stem)
            if ex and ex["track"] == track_name and path.suffix == ex["attempt"].suffix:
                moves.append((path, ex["attempt"]))
            elif path.name != ".gitkeep":
                moves.append((path, folder / "scratch" / path.name))
        cache = folder / "__pycache__"
        if cache.is_dir():
            shutil.rmtree(cache)
    old_history = WORKSPACE / HISTORY_DIR
    if old_history.is_dir():
        for path in sorted(p for p in old_history.iterdir() if p.is_file()):
            m = HISTORY_STAMP_RE.match(path.name)
            ex = exercises.get(m.group("slug")) if m else None
            if ex:
                moves.append((path, ex["attempt"].parent / HISTORY_DIR / path.name))
    moved = 0
    for src, dest in moves:
        if dest.exists():
            print(f"  migrate: kept {src.relative_to(ROOT).as_posix()} "
                  f"({dest.relative_to(ROOT).as_posix()} already exists)")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), dest)
        moved += 1
        if verbose:
            print(f"  moved {src.relative_to(ROOT).as_posix()} -> {dest.relative_to(ROOT).as_posix()}")
    if old_history.is_dir() and not any(old_history.iterdir()):
        old_history.rmdir()
    if moved:
        print(f"Workspace reorganised by module: {moved} file(s) moved.")
    return moved


def cmd_migrate(args) -> None:
    if not migrate_workspace(verbose=True):
        print("Workspace already in the per-module layout.")


HELP = """Code Dojo commands (python dojo.py <command>). New here? python dojo.py setup

  setup [--fresh]          START HERE: installs if needed, asks your mode, target level, time per
                           day, tracks and level, checks everything, then says what the tutor does next
                           (--yes with --name, --mode, --target-level, --minutes, --rest, --tracks, ...:
                           no questions; the tutor uses this after asking you in chat)
  install                  create .venv and install pytest (setup does this for you)
  doctor                   check Python, venv, pytest and profile
  today                    today's plan: time, week balance, redo queue, next exercises
  list [module]            all exercises with their status
  start <item> [--fresh]   start the timer; for a dojo exercise also create
                           workspace/<track>/<module>/<item>.py (earlier attempts go to .history/)
  test <item> [--debug]    run that exercise's tests against your workspace file
                           (--debug: in-process, for editor breakpoints)
  done <item> --hints N    stop the timer, run tests, log, schedule the next redo
       [--gave-up] [--minutes M] [--level easy --pattern hashmap]   (for LeetCode etc.)
       --skipped plan,predict    process steps left out (understand, example, plan, predict, test, reflect)
       --credit M                minutes lost to a tutor misunderstanding (off the solve time, still logged)
       mocks: done mock_<date> --kind mock --result strong|pass|fail --no-review
  log <kind> <minutes>     log time without a timer: study, reading, drill, mock, project
  pause / resume [item]    stop the clock while talking something through, then continue
  clarify <item>           the interviewer's answers (edge cases); list your own first
  cancel <item>            discard a running timer
  mark <items/modules> --box N   seed the redo schedule for things you already know
  mistake <item> "what went wrong" "correct form"
  export [--to user@host:path]   zip progress/ and workspace/; copy over SSH with --to
                                 (--to rclone:gdrive:CodeDojo uploads to Google Drive)
  drive-setup [--remote gdrive] [--folder CodeDojo]   one-time Google Drive sign-in for export
  import <zip> [--force]         restore an export on this machine
  week [--write]           weekly report (writes progress/weekly/YYYY-Www.md)
  stats                    modules, patterns, fluency gates (and time by track)
  modules                  your modules: assigned, excluded, before your start, or planned
  update [--yes]           show what the shared repo changed (and which files run code), apply it
                           after a yes, then list the new or changed exercises in your tracks
  changes [--ack [slugs]]  new, changed or removed exercises since you were last asked;
                           --ack records them as seen (all, or the slugs given)
  settings [key=value ...] show every setting, or change any (minutes=mon=60,sat=0, mode=hobby,
                           skip_modules=m08,m09, ...; key+=value adds to a list, key-=value removes);
                           --review suggests changes from your log
  mix [track=N ...] [--priority TEXT]   share of new material per track (0 = redos only);
                           no arguments shows the current mix
  sync                     find work done without logging it
  primm <module> [topic]   create workspace/<track>/<module>/primm/ (and an empty <topic> file);
                           with a topic, starts a lesson timer: end it with `done lesson:<topic>`
                           for a teach-me lesson
  migrate                  move files from the old flat workspace into module folders (also automatic)
  verify [items]           (maintainers) stubs fail, solutions pass
"""


def main() -> None:
    parser = argparse.ArgumentParser(prog="dojo", add_help=False)
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("setup"); p.add_argument("--fresh", action="store_true")
    p.add_argument("--yes", action="store_true", help="no questions: flags, else current or default values")
    for flag in ("--name", "--goal", "--mode", "--target-level", "--level", "--start-date",
                 "--target-date", "--rest", "--flexible", "--tracks"):
        p.add_argument(flag)
    p.add_argument("--minutes", help="one number for every day, or per day: mon=60,tue=90,...")
    sub.add_parser("install")
    sub.add_parser("doctor")
    sub.add_parser("today")
    sub.add_parser("brief")
    p = sub.add_parser("list"); p.add_argument("module", nargs="?")
    p = sub.add_parser("start"); p.add_argument("item"); p.add_argument("--fresh", action="store_true")
    p = sub.add_parser("test"); p.add_argument("item"); p.add_argument("--solution", action="store_true")
    p.add_argument("--debug", action="store_true")
    p = sub.add_parser("done")
    p.add_argument("item")
    p.add_argument("--hints", type=int, default=0)
    p.add_argument("--minutes", type=float)
    p.add_argument("--credit", type=float, default=0,
                   help="minutes lost to a tutor misunderstanding: taken off the solve time")
    p.add_argument("--gave-up", action="store_true")
    p.add_argument("--result", choices=["solved", "failed", "strong", "pass", "fail"])
    p.add_argument("--kind", choices=KINDS)
    p.add_argument("--level", choices=list(TARGETS))
    p.add_argument("--target", type=int)
    p.add_argument("--pattern")
    p.add_argument("--module")
    p.add_argument("--note")
    p.add_argument("--date")
    p.add_argument("--no-review", action="store_true")
    p.add_argument("--skipped", help="comma-separated process steps left out: " + ",".join(STEPS))
    p = sub.add_parser("log")
    p.add_argument("kind", choices=KINDS)
    p.add_argument("minutes", type=float)
    p.add_argument("item", nargs="?")
    p.add_argument("--hints", type=int, default=0)
    p.add_argument("--result")
    p.add_argument("--pattern")
    p.add_argument("--level")
    p.add_argument("--note")
    p.add_argument("--date")
    p = sub.add_parser("cancel"); p.add_argument("item")
    p = sub.add_parser("pause"); p.add_argument("item", nargs="?")
    p = sub.add_parser("resume"); p.add_argument("item", nargs="?")
    p = sub.add_parser("clarify"); p.add_argument("item")
    p = sub.add_parser("mark"); p.add_argument("items", nargs="+"); p.add_argument("--box", type=int, default=2)
    p = sub.add_parser("mistake"); p.add_argument("item"); p.add_argument("what"); p.add_argument("fix")
    p = sub.add_parser("week"); p.add_argument("--write", action="store_true")
    p.add_argument("--force", action="store_true"); p.add_argument("--date")
    p = sub.add_parser("export"); p.add_argument("--to"); p.add_argument("--out")
    p = sub.add_parser("drive-setup"); p.add_argument("--remote", default="gdrive"); p.add_argument("--folder", default="CodeDojo")
    p = sub.add_parser("import"); p.add_argument("archive"); p.add_argument("--force", action="store_true")
    sub.add_parser("stats")
    p = sub.add_parser("changes"); p.add_argument("--ack", nargs="*")
    p = sub.add_parser("update"); p.add_argument("--yes", action="store_true")
    sub.add_parser("modules")
    p = sub.add_parser("settings"); p.add_argument("changes", nargs="*"); p.add_argument("--review", action="store_true")
    p = sub.add_parser("mix"); p.add_argument("shares", nargs="*"); p.add_argument("--priority")
    sub.add_parser("sync")
    p = sub.add_parser("verify"); p.add_argument("items", nargs="*")
    p = sub.add_parser("primm"); p.add_argument("module"); p.add_argument("topic", nargs="?")
    sub.add_parser("migrate")
    sub.add_parser("help")

    args = parser.parse_args()
    commands = {
        "setup": cmd_setup, "install": cmd_install, "doctor": cmd_doctor, "today": cmd_today, "list": cmd_list,
        "start": cmd_start, "test": cmd_test, "done": cmd_done, "log": cmd_log,
        "cancel": cmd_cancel, "pause": cmd_pause, "resume": cmd_resume, "clarify": cmd_clarify, "mistake": cmd_mistake, "mark": cmd_mark, "export": cmd_export, "drive-setup": cmd_drive_setup, "import": cmd_import, "week": cmd_week, "stats": cmd_stats, "mix": cmd_mix, "settings": cmd_settings, "changes": cmd_changes, "update": cmd_update, "modules": cmd_modules,
        "sync": cmd_sync, "verify": cmd_verify, "primm": cmd_primm, "migrate": cmd_migrate,
    }
    if args.cmd in ("brief", "today", "start", "test", "done", "sync", "primm"):
        migrate_workspace(verbose=False)  # older checkouts kept every attempt in one flat folder
    if args.cmd == "brief":
        cmd_today(args, brief=True)
    elif args.cmd in commands:
        commands[args.cmd](args)
    else:
        print(HELP)


if __name__ == "__main__":
    main()
