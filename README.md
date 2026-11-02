# Code Dojo

A personal training system for becoming a strong engineer: learn to **write** code from a
blank file, **understand** code you did not write, and **perform** in live-coding interviews.
Claude Code acts as a tutor that explains, questions, hints and reviews, but never writes your
code for you.

It works for anyone and any subject: choose your tracks and your weekly hours, run a
placement, and the dojo plans, measures and adapts around you. A complete Python track ships
with it (fundamentals, reading and debugging code, data structures and algorithms, projects,
interview practice).

## Why it works

- **Retrieval and spacing.** Every exercise comes back from a blank file after 1, 3, 7, 14, 30
  and 60 days, sooner if it went badly.
- **Deliberate practice with instant feedback.** Every exercise has tests and a target time;
  time and hints are logged for every attempt.
- **Read as much as you write.** Predict, trace, debug and review drills, including spotting
  bugs in AI-written code.
- **Build things.** A ladder of projects with requirements but no step-by-step guide.
- **A method you cannot skip by accident.** Checklists for every activity; the tutor asks you
  to think out loud and flags skipped steps, and the weekly report scores your process.
- **Train the performance.** Talk-aloud timed problems most days and a mock interview every week.
- **AI as tutor, not ghostwriter.** The evidence and the rules are in [docs/METHOD.md](docs/METHOD.md).

## Quick start

Requires Python 3.10+ (on Windows use `py` or `python`; on macOS and Linux `python3`).

```bash
git clone <this repo> code-dojo
cd code-dojo
python dojo.py install     # creates .venv with pytest (any OS)
python dojo.py setup       # your name, minutes per weekday, rest days, tracks, level
python dojo.py doctor      # checks everything
claude                     # the tutor; then say: assess me
```

Full instructions, the VS Code and Zed debugger setup, and moving between machines: [docs/SETUP.md](docs/SETUP.md).

## A day in the dojo

```bash
python dojo.py today                 # time today and this week, redo queue, next exercises
python dojo.py start parse_pairs     # timer + workspace/python/parse_pairs.py
python dojo.py test parse_pairs      # run the tests against your file
python dojo.py done parse_pairs --hints 1
python dojo.py week --write          # weekly report
```

Or just talk to the tutor (`start parse_pairs`, `I'm stuck`, `teach me generators`,
`mock interview`); it runs the tracker for you. Session templates for 30 minutes to 3 hours:
[docs/DAILY_SESSION.md](docs/DAILY_SESSION.md). All tutor commands: [docs/TUTOR.md](docs/TUTOR.md).

## What is where

```text
code-dojo/
├── dojo.py                  tracker: timers, tests, redo schedule, week balance, reports, export
├── CLAUDE.md                tutor-mode rules for Claude Code
├── .claude/skills/          dojo-session, dojo-assess, dojo-teach, dojo-mock, dojo-drill,
│                            dojo-weekly, dojo-new-exercise
├── .claude/agents/          problem-setter, code-reviewer, progress-coach
├── .claude-plugin/          optional: the same skills and agents as an installable plugin
├── docs/                    METHOD, CHECKLISTS, DAILY_SESSION, TRACKS, TUTOR, INTERVIEW_PLAYBOOK, SETUP
├── tracks/
│   ├── python/              the Python track: README (phases, modules, milestones), modules,
│   │                        projects/
│   ├── cpp/                 placeholder for an optional future track
│   └── ros/                 placeholder for an optional future track
├── progress/                YOUR data (gitignored): profile, PLAN, BASELINE, log, redo
│                            schedule, mistakes, cheat sheet, weekly reports, mocks
└── workspace/               YOUR attempts and projects (gitignored)
```

## Your data stays yours

`progress/` and `workspace/` never go into git. Back them up or move them with
`python dojo.py export` (a zip), or straight to another machine over SSH:
`python dojo.py export --to user@host:path`, then `python dojo.py import <zip>` there.

## Make it yours, or share it

- **Tracks are optional.** Add any subject with a `track.json` and modules; see
  [docs/TRACKS.md](docs/TRACKS.md). The tutor can generate verified exercises for it.
- **Friends** get a clean copy (personal data is gitignored), run the quick start, then
  `assess me`: the placement imports what they already know and sets their own plan.
- **Plugin (optional).** The skills and agents also install as a Claude Code plugin from this
  repo (`/plugin marketplace add <repo>`, then `/plugin install code-dojo@code-dojo`), for
  example to use the drills and lessons in another project. Inside this repo you do not need
  it: everything loads from `.claude/` automatically. Do not install both in the same folder,
  or each skill appears twice.

## Contributing exercises

`python dojo.py verify` checks that every stub fails and every reference solution passes. New
exercises follow the format in [docs/TRACKS.md](docs/TRACKS.md).
