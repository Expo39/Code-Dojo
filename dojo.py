#!/usr/bin/env python3
"""Code Dojo: tracker, scheduler and exercise runner.

Standard library only, works on Linux, macOS and Windows.
Run `python dojo.py help` for the commands (use `python3` on Linux/macOS if
`python` is not found).
"""

from __future__ import annotations

import argparse
import csv
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
HISTORY = WORKSPACE / ".history"

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

DEFAULT_PROFILE = {
    "learner": "",
    "start_date": "",
    "target_date": "",
    "goal": "Pass live-coding interviews in Python",
    "minutes": {"mon": 180, "tue": 180, "wed": 180, "thu": 180,
                "fri": 180, "sat": 180, "sun": 0},
    "flexible_rest_day": True,
    "level": "beginner",
    "start_module": "",
    "skip_modules": [],
    "tracks": [],
    "export_target": "",
}

MISTAKES_HEADER = """# Mistakes log

One row per mistake. The tutor fills this in (`python dojo.py mistake ...`).
Read it at the end of each week; the weekly review turns repeats into drills.

| Date | Item | What went wrong | Correct form |
| --- | --- | --- | --- |
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


def cmd_setup(args) -> None:
    existing = read_json(PROFILE, None)
    if existing and not args.fresh:
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

    print("\nCode Dojo setup. All of this can be changed later with `python dojo.py setup`.\n")
    profile["learner"] = ask("Your name", profile["learner"] or os.environ.get("USER", os.environ.get("USERNAME", "")))
    profile["goal"] = ask("Your goal in one line", profile["goal"])
    profile["start_date"] = ask("Start date (YYYY-MM-DD)", profile["start_date"] or today().isoformat())
    profile["target_date"] = ask("Target date, e.g. an interview (YYYY-MM-DD, empty for none)", profile["target_date"])

    print("\nHow many minutes can you train on each day? 0 = rest day.")
    print("Tip: enter one number for every day (e.g. 180), then adjust single days.")
    same = ask("Minutes for every day (empty to set day by day)", "")
    minutes = dict(profile["minutes"])
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
    flex = ask("Flexible rest day? Training on a rest day counts towards the week (y/n)",
               "y" if profile["flexible_rest_day"] else "n")
    profile["flexible_rest_day"] = flex.lower().startswith("y")

    available = load_tracks(active_only=False)
    print("\nTracks available: " + ", ".join(f"{k} ({v['name']})" for k, v in available.items()))
    chosen = ask("Tracks to follow, comma separated (empty = all)", ",".join(profile["tracks"]))
    profile["tracks"] = [t.strip() for t in chosen.split(",") if t.strip() in available]
    write_json(PROFILE, profile)

    print("\nWhere are you now? (The tutor can refine this: run /dojo-assess in Claude Code.)")
    print("  beginner     = new to writing code by hand")
    print("  intermediate = can write small programs, slow or needs hints")
    print("  advanced     = fluent in Python basics, here for patterns and interviews")
    profile["level"] = ask("Level", profile["level"])
    modules = sorted({ex["module"] for ex in discover().values()})
    print("Modules: " + ", ".join(modules))
    profile["start_module"] = ask("Start at module (empty = the first)", profile["start_module"])
    skip = ask("Modules you already know well, comma separated (empty for none)",
               ",".join(profile["skip_modules"]))
    profile["skip_modules"] = [m.strip() for m in skip.split(",") if m.strip()]

    PROGRESS.mkdir(exist_ok=True)
    WORKSPACE.mkdir(exist_ok=True)
    write_json(PROFILE, profile)
    ensure_files()
    total = weekly_target(profile)
    print(f"\nSaved. Weekly target: {fmt_min(total)} over "
          f"{sum(1 for d in DAYS if minutes[d] > 0)} days.")
    print("Next: `python dojo.py doctor` to check the setup, then `python dojo.py today`.")


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
            if any(part.startswith(".") or part == "tests" for part in path.relative_to(track["dir"]).parts[:-1]):
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
            found[slug] = {
                "slug": slug,
                "stub": path,
                "solution": path.parent / track["solution_file"].format(slug=slug),
                "test": path.parent / track["test_file"].format(slug=slug),
                "clarify": clarify,
                "attempt": WORKSPACE / track_name / f"{slug}{ext}",
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

def cmd_install(args) -> None:
    """Create .venv and install requirements, the same way on every OS."""
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
    print("Done. Next: python dojo.py setup")


def cmd_export(args) -> None:
    """Zip all personal data (progress/ and workspace/), optionally copy it over SSH."""
    import zipfile
    profile = load_profile(required=False)
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
    target = args.to or profile.get("export_target")
    if target:
        if shutil.which("scp") is None:
            die("scp not found. Install OpenSSH (built into Windows 10+, macOS and most Linux) "
                "or copy the zip by hand.")
        print(f"Copying to {target} ...")
        result = subprocess.run(["scp", str(archive), target])
        if result.returncode != 0:
            die("scp failed; the zip is still on this machine.")
        print("Copied. On the other device: python dojo.py import <zip>")


def cmd_import(args) -> None:
    """Restore progress/ and workspace/ from an export zip."""
    import zipfile
    archive = Path(args.archive).expanduser()
    if not archive.exists():
        die(f"No such file: {archive}")
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        bad = [n for n in names if not (n.startswith("progress/") or n.startswith("workspace/"))
               or ".." in Path(n).parts]
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
            HISTORY.mkdir(parents=True, exist_ok=True)
            stamp = now().strftime("%Y%m%d_%H%M")
            shutil.move(str(attempt), HISTORY / f"{args.item}_{stamp}{attempt.suffix}")
        if not attempt.exists():
            shutil.copy(ex["stub"], attempt)
            print(f"Fresh file: {shown}")
            if redo:
                print("Redo from a blank file: do not open .history/ or old notes.")
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
    if args.debug:
        sys.exit(debug_in_process(ex, target))
    passed = run_exercise(ex, target=target)
    if passed is None:
        die(f"Track '{ex['track']}' has no test command; check your work with the tutor.")
    sys.exit(0 if passed else 1)


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
    on = parse_date(args.date) if args.date else today()
    skipped = [x.strip().lower() for x in (args.skipped or "").split(",") if x.strip()]
    unknown = [x for x in skipped if x not in STEPS]
    if unknown:
        die(f"Unknown step(s): {', '.join(unknown)}. Steps: {', '.join(STEPS)}")
    append_log({"date": on.isoformat(), "item": args.item, "kind": kind, "module": module,
                "pattern": pattern, "level": level, "minutes": round(minutes, 1),
                "target": target or "", "hints": args.hints, "result": result,
                "ratio": ratio if ratio is not None else "",
                "skipped": ",".join(skipped), "note": args.note or ""})

    verdict = f"{args.item}: {result} in {fmt_min(minutes)}"
    if ratio is not None:
        verdict += f" ({ratio}x target {target}m)"
    verdict += f", hints {args.hints}."
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


def in_scope(ex: dict, profile: dict) -> bool:
    """False for modules the learner skipped or that come before their start module."""
    module = ex["module"]
    if any(module.startswith(s) for s in profile.get("skip_modules", [])):
        return False
    start = profile.get("start_module", "")
    return not start or module >= start


def next_new(profile: dict, limit: int = 3) -> list[dict]:
    reviews = read_json(REVIEWS, {})
    return [ex for slug, ex in discover().items()
            if slug not in reviews and in_scope(ex, profile)][:limit]


def cmd_today(args, brief: bool = False) -> None:
    profile = load_profile(required=not brief)
    if not PROFILE.exists():
        print("[dojo] No profile yet: ask the learner to run `python dojo.py setup`.")
        return
    rows = read_log()
    on = today()
    plan = planned_minutes(profile, on)
    done_today = minutes_on(rows, on)
    wk = week_numbers(profile, rows, on)
    due = due_items(on)
    timers = read_json(TIMER, {})
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
        extra = min(-gap / len(wk["remaining_days"]), 60)
        lines.append(f"  Catch-up: add about {fmt_min(extra)} on each of the remaining "
                     f"{len(wk['remaining_days'])} training days, or use the rest day"
                     + (" (flexible)." if profile["flexible_rest_day"] else "."))
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
    if upcoming:
        lines.append("Next new: " + ", ".join(f"{e['slug']} ({e['module']})" for e in upcoming) + ".")
    weak = [(p, s) for p, s in recent_stats(rows, 14, on).items()
            if s["n"] >= 2 and (s["ratio"] > 1.5 or s["hints"] > 1.5)]
    if weak:
        lines.append("Weak spots (last 14 days): " + ", ".join(
            f"{p} ({s['ratio']:.1f}x, {s['hints']:.1f} hints)" for p, s in weak[:5]) + ".")
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


HELP = """Code Dojo commands (python dojo.py <command>):

  install                  create .venv and install pytest (any OS)
  setup [--fresh]          create or edit your profile (time per day, rest days, target date)
  doctor                   check Python, venv, pytest and profile
  today                    today's plan: time, week balance, redo queue, next exercises
  list [module]            all exercises with their status
  start <item> [--fresh]   start the timer; for a dojo exercise also create workspace/<item>.py
  test <item> [--debug]    run that exercise's tests against your workspace file
                           (--debug: in-process, for editor breakpoints)
  done <item> --hints N    stop the timer, run tests, log, schedule the next redo
       [--gave-up] [--minutes M] [--level easy --pattern hashmap]   (for LeetCode etc.)
       --skipped plan,predict    process steps left out (understand, example, plan, predict, test, reflect)
       mocks: done mock_<date> --kind mock --result strong|pass|fail --no-review
  log <kind> <minutes>     log time without a timer: study, reading, drill, mock, project
  pause / resume [item]    stop the clock while talking something through, then continue
  clarify <item>           the interviewer's answers (edge cases); list your own first
  cancel <item>            discard a running timer
  mark <items/modules> --box N   seed the redo schedule for things you already know
  mistake <item> "what went wrong" "correct form"
  export [--to user@host:path]   zip progress/ and workspace/; copy over SSH with --to
  import <zip> [--force]         restore an export on this machine
  week [--write]           weekly report (writes progress/weekly/YYYY-Www.md)
  stats                    modules, patterns, fluency gates
  sync                     find work done without logging it
  verify [items]           (maintainers) stubs fail, solutions pass
"""


def main() -> None:
    parser = argparse.ArgumentParser(prog="dojo", add_help=False)
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("setup"); p.add_argument("--fresh", action="store_true")
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
    p = sub.add_parser("import"); p.add_argument("archive"); p.add_argument("--force", action="store_true")
    sub.add_parser("stats")
    sub.add_parser("sync")
    p = sub.add_parser("verify"); p.add_argument("items", nargs="*")
    sub.add_parser("help")

    args = parser.parse_args()
    commands = {
        "setup": cmd_setup, "install": cmd_install, "doctor": cmd_doctor, "today": cmd_today, "list": cmd_list,
        "start": cmd_start, "test": cmd_test, "done": cmd_done, "log": cmd_log,
        "cancel": cmd_cancel, "pause": cmd_pause, "resume": cmd_resume, "clarify": cmd_clarify, "mistake": cmd_mistake, "mark": cmd_mark, "export": cmd_export, "import": cmd_import, "week": cmd_week, "stats": cmd_stats,
        "sync": cmd_sync, "verify": cmd_verify,
    }
    if args.cmd == "brief":
        cmd_today(args, brief=True)
    elif args.cmd in commands:
        commands[args.cmd](args)
    else:
        print(HELP)


if __name__ == "__main__":
    main()
