"""The command line: help text and argument parsing."""

from __future__ import annotations

import argparse

from .core import KINDS, PROGRESS, STEPS, TARGETS
from .updates import cmd_changes, cmd_update
from .migrate import cmd_migrate, migrate_dates, migrate_workspace
from .setup import cmd_doctor, cmd_install, cmd_settings, cmd_setup
from .transfer import cmd_drive_setup, cmd_export, cmd_import
from .practice import (
    cmd_cancel, cmd_clarify, cmd_debug, cmd_done, cmd_list, cmd_log, cmd_mark, cmd_mistake,
    cmd_pause, cmd_primm, cmd_resume, cmd_session, cmd_start, cmd_sync, cmd_test, cmd_verify
)
from .reports import cmd_mix, cmd_modules, cmd_stats, cmd_today, cmd_week


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
  debug <file>             debug any open file with editor breakpoints: an exercise runs its
                           tests, a drill or mock its tests/ file, anything else runs as a script
  done <item> --hints N    stop the timer, run tests, log, schedule the next redo
       [--gave-up] [--minutes M] [--level easy --pattern hashmap]   (for LeetCode etc.)
       --skipped plan,predict    process steps left out (understand, example, plan, predict, test, reflect)
       --credit M                minutes lost to a tutor misunderstanding (off the solve time, still logged)
       mocks: done <problem>_<date> --kind mock --result strong|pass|fail --no-review
  log <kind> <minutes>     log time without a timer: study, reading, drill, mock, project
  pause / resume [item]    stop the clock while talking something through, then continue
  session start|pause|resume|status|end
                           the session clock: at `end`, training time outside exercise
                           timers (warm-up, explanations, feedback) is logged as study;
                           pause it for breaks and anything that is not training
  clarify <item>           the interviewer's answers (edge cases); list your own first
  cancel <item>            discard a running timer
  mark <items/modules> --box N   seed the redo schedule for things you already know
  mistake <item> "what went wrong" "correct form"
  export [--to user@host:path]   zip progress/ and workspace/; copy over SSH with --to
                                 (--to rclone:gdrive:CodeDojo uploads to Google Drive)
  drive-setup [--remote gdrive] [--folder CodeDojo]   one-time Google Drive sign-in for export
  import <zip> [--force]         restore an export on this machine
  week [--write]           weekly report (writes progress/weekly/week_<Monday DD-MM-YYYY>.md)
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
  migrate                  move older layouts into the current one: module folders, drills/<type>/
                           and mocks/<type>/ (also automatic)
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
    p = sub.add_parser("debug"); p.add_argument("file")
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
    p = sub.add_parser("session"); p.add_argument("action", choices=["start", "pause", "resume", "status", "end"])
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
        "start": cmd_start, "test": cmd_test, "debug": cmd_debug, "done": cmd_done, "log": cmd_log,
        "cancel": cmd_cancel, "pause": cmd_pause, "resume": cmd_resume, "clarify": cmd_clarify, "session": cmd_session, "mistake": cmd_mistake, "mark": cmd_mark, "export": cmd_export, "drive-setup": cmd_drive_setup, "import": cmd_import, "week": cmd_week, "stats": cmd_stats, "mix": cmd_mix, "settings": cmd_settings, "changes": cmd_changes, "update": cmd_update, "modules": cmd_modules,
        "sync": cmd_sync, "verify": cmd_verify, "primm": cmd_primm, "migrate": cmd_migrate,
    }
    if args.cmd in ("brief", "today", "start", "test", "done", "sync", "primm"):
        migrate_workspace(verbose=False)  # older checkouts kept every attempt in one flat folder
    if args.cmd not in ("help", "migrate") and PROGRESS.exists():
        migrate_dates(verbose=False)  # older data used ISO dates (YYYY-MM-DD)
    if args.cmd == "brief":
        cmd_today(args, brief=True)
    elif args.cmd in commands:
        commands[args.cmd](args)
    else:
        print(HELP)
