"""Setup, install, doctor and settings."""

from __future__ import annotations

import os
import shutil
import statistics
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

from .core import (
    DAYS, DEFAULT_PROFILE, LEVELS, MODES, PROFILE, PROGRESS, ROOT, STAMP_FMT, WORKSPACE, ask, die,
    fmt_date, fmt_min, load_profile, now, parse_date, read_json, today, week_start, weekly_target,
    write_json
)
from .data import ensure_files, minutes_on, read_log
from .tracks import discover, find_venv_python, load_tracks, venv_python
from .planning import effective_mix, module_overview, print_modules


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
        stamp = now().strftime(STAMP_FMT)
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
    profile["start_date"] = value(args.start_date, "Start date (DD/MM/YYYY)",
                                  profile["start_date"] or fmt_date(today()))
    profile["target_date"] = value(args.target_date, "Target date, e.g. an interview (DD/MM/YYYY, empty for none)",
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
