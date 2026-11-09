"""Practice commands: exercises, timers, the session clock, logging, lessons and verification."""

from __future__ import annotations

import os
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

from .core import (
    CHECKLIST, HISTORY_DIR, INTERVALS, LESSON_PREFIX, MASTERED_BOX, MISTAKES, PRIMM_DIR, PROBE_PREFIX,
    REVIEWS, ROOT, SESSION, STEPS, TARGETS, TIMER, WORKSPACE, active_track_names, die, fmt_date,
    fmt_min, mistakes_header, now, parse_date, read_json, today, track_progress, write_json
)
from .data import (
    append_log, due_items, ensure_files, minutes_on, paused_minutes, pick_timer, read_log,
    schedule, session_gap, timer_minutes, timer_of
)
from .tracks import (
    debug_in_process, discover, get_exercise, load_tracks, modules_by_name, run_exercise, side_track,
    test_slug, warn_if_unsaved
)
from .planning import interleave_due


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
        due = [k for k, _ in interleave_due(due_items(today())) if k != args.item]
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
            stamp = now().strftime("%d%m%Y_%H%M")
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
    elif args.item.startswith(PROBE_PREFIX):
        print(f"Probe timer started. End it with: python dojo.py done {args.item}")
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


def cmd_debug(args) -> None:
    """Debug whatever file is open in the editor, so its breakpoints work.

    A dojo exercise runs its tests in-process; a drill or mock (drills/<type>/,
    mocks/<type>/) runs its test file, found with the track's test_file pattern, as does an
    open test file; anything else (a lesson, a project file) runs as a script. Python tracks
    only: other languages debug with their own tools.
    """
    path = Path(args.file).resolve()
    if not path.is_file():
        die(f"No such file: {args.file}")
    for ex in discover().values():
        if path in (ex["attempt"].resolve(), ex["stub"].resolve()):
            sys.exit(debug_in_process(ex, None))
    track = side_track(path)
    if track and not any("pytest" in part for part in track.get("test_command") or []):
        die(f"debug works for pytest-based tracks; debug {track['name']} with its own tools.")
    tests = None
    if track:
        tests = path if test_slug(track, path) else path.parent / track["test_file"].format(slug=path.stem)
    if tests and tests.is_file():
        try:
            import pytest
        except ImportError:
            die("pytest is not importable here: start the debugger with the .venv interpreter.")
        os.chdir(ROOT)
        sys.exit(pytest.main(["-q", "--no-header", "-p", "no:cacheprovider", str(tests)]))
    if path.suffix != ".py":
        die(f"No tests found for {path.name}; debug it with its own language's tools.")
    import runpy
    os.chdir(path.parent)
    sys.path.insert(0, str(path.parent))
    runpy.run_path(str(path), run_name="__main__")


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

    if args.item.startswith((LESSON_PREFIX, PROBE_PREFIX)):
        # A PRIMM lesson or a probe: training time, but no target, no tests and no redo schedule.
        probe = args.item.startswith(PROBE_PREFIX)
        topic = args.item.split(":", 1)[1]
        module = timer_of(started).get("module", "") if started else ""
        append_log({"date": fmt_date(on), "item": f"probe_{topic}" if probe else topic, "kind": "study",
                    "module": module, "minutes": round(minutes + credit + paused, 1),
                    "note": "probe" if probe else "PRIMM lesson"})
        print(f"{'Probe' if probe else 'Lesson'} '{topic}': {fmt_min(minutes + credit + paused)} logged as study.")
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
    append_log({"date": fmt_date(on), "item": args.item, "kind": kind, "module": module,
                "pattern": pattern, "level": level, "minutes": round(minutes, 1),
                "target": target or "", "hints": args.hints, "result": result,
                "ratio": ratio if ratio is not None else "",
                "skipped": ",".join(skipped), "note": args.note or "",
                "confidence": confidence_value(args), "prediction": args.prediction or ""})
    if credit:
        # Time lost to a tutor misunderstanding: off the solve time, still counted as training.
        append_log({"date": fmt_date(on), "item": args.item, "kind": "study",
                    "minutes": round(credit, 1), "note": "credit: tutor misunderstanding"})
    if paused >= 0.5:
        # Clock paused for a discussion: off the solve time, still counted as training.
        append_log({"date": fmt_date(on), "item": args.item, "kind": "study",
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


def confidence_value(args) -> str:
    """The learner's stated confidence (0-100) as logged, or empty when it was not asked."""
    if args.confidence is None:
        return ""
    if not 0 <= args.confidence <= 100:
        die("--confidence is a percentage from 0 to 100.")
    return str(args.confidence)


def cmd_log(args) -> None:
    ensure_files()
    on = parse_date(args.date) if args.date else today()
    append_log({"date": fmt_date(on), "item": args.item or args.kind, "kind": args.kind,
                "minutes": args.minutes, "hints": args.hints, "result": args.result or "",
                "pattern": args.pattern or "", "level": args.level or "", "note": args.note or "",
                "confidence": confidence_value(args), "prediction": args.prediction or ""})
    print(f"Logged {fmt_min(args.minutes)} of {args.kind} on {fmt_date(on)}.")


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


def cmd_session(args) -> None:
    """Session clock: counts the whole training session, so time outside exercise timers
    (warm-up, explanations, feedback, discussing a concept) is logged as study at the end.
    Pause it for anything that is not training: breaks, dojo maintenance, being away."""
    ensure_files()
    session = read_json(SESSION, None)
    rows = read_log()
    if args.action == "start":
        if session:
            die("A session is already running: `session end` first.")
        write_json(SESSION, {"date": fmt_date(today()), "start": now().isoformat(),
                             "paused_total": 0.0, "paused_at": None,
                             "logged_at_start": minutes_on(rows, today())})
        print("Session clock started. Pause it for breaks and anything that is not training.")
        return
    if not session:
        die("No session running: `python dojo.py session start`.")
    if args.action == "pause":
        if session["paused_at"]:
            die("The session is already paused.")
        session["paused_at"] = now().isoformat()
        write_json(SESSION, session)
        print(f"Session paused at {fmt_min(timer_minutes(session))}.")
    elif args.action == "resume":
        if not session["paused_at"]:
            die("The session is not paused.")
        session["paused_total"] += (now() - datetime.fromisoformat(session["paused_at"])).total_seconds()
        session["paused_at"] = None
        write_json(SESSION, session)
        print(f"Session resumed ({fmt_min(timer_minutes(session))} so far).")
    elif args.action == "status":
        clock, logged, gap = session_gap(session, rows)
        print(f"Session {fmt_min(clock)}{' (PAUSED)' if session['paused_at'] else ''}: "
              f"{fmt_min(logged)} logged by timers, {fmt_min(gap)} outside them.")
    elif args.action == "end":
        if read_json(TIMER, {}):
            die("A timer is still running: `done` or `cancel` it first.")
        clock, logged, gap = session_gap(session, rows)
        if gap >= 1:
            append_log({"date": session["date"], "item": "session", "kind": "study",
                        "minutes": round(gap, 1), "hints": 0,
                        "note": "training time outside timers: warm-up, explanations, feedback"})
        SESSION.unlink()
        print(f"Session ended: {fmt_min(clock)} in total, {fmt_min(logged)} from timers, "
              f"{fmt_min(gap)} added as study.")


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
        card.update({"box": box, "grade": "placed", "last": fmt_date(on),
                     "due": fmt_date(on + timedelta(days=INTERVALS[box]))})
        reviews[slug] = card
    write_json(REVIEWS, reviews)
    print(f"Placed {len(slugs)} exercises in box {box} (first redo in {INTERVALS[box]} days).")


def cmd_mistake(args) -> None:
    """Log a mistake in the shared log (--shared: holds in any language) or a track's log: the
    exercise's track when the item is one, else --track, else the learner's first track."""
    ensure_files()
    if args.shared:
        path = MISTAKES
    else:
        ex = discover(active_only=False).get(args.item)
        track = args.track or (ex["track"] if ex else active_track_names()[0])
        if track not in load_tracks(active_only=False):
            die(f"No track called '{track}'.")
        folder = track_progress(track)
        folder.mkdir(exist_ok=True)
        path = folder / "mistakes.md"
        if not path.exists():
            path.write_text(mistakes_header(track), encoding="utf-8")
    clean = [s.replace("|", "/").replace("\n", " ") for s in (args.item, args.what, args.fix)]
    with path.open("a", encoding="utf-8") as f:
        f.write(f"| {fmt_date(today())} | {clean[0]} | {clean[1]} | {clean[2]} |\n")
    print(f"Mistake logged in {path.relative_to(ROOT).as_posix()}.")


def cmd_sync(args) -> None:
    """Find workspace files changed since they were last logged."""
    ensure_files()
    rows = read_log()
    last_logged: dict[str, datetime] = {}
    for r in rows:
        last_logged[r["item"]] = datetime.combine(parse_date(r["date"]), datetime.max.time())
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
            print(f"  {slug}: edited {changed:%d/%m/%Y %H:%M}, not logged, tests {state}.")
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
