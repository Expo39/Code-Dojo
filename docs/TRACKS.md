# Tracks, plans and adding your own

Code Dojo is a training system, not a fixed course. **Everything is optional.** A learner
chooses one or more *tracks* (subjects), and keeps a personal *plan* with their own goals,
skill tree and dates. The repo ships with a Python track as a complete example; anyone can add
a track for any subject (another language, a framework, maths, even a non-coding skill).

## What is shared and what is personal

| Shared (in git, the same for everyone) | Personal (in `progress/` and `workspace/`, gitignored, never pushed) |
| --- | --- |
| `dojo.py` (tracker), `conftest.py` | `profile.json`: name, mode, target level, time per day, rest days, target date, level, tracks, mix (`python dojo.py settings` shows it) |
| `tracks/<track>/`: syllabus, exercises, tests, reference solutions | `PLAN.md`: goals, roadmap (track order and mix), skill tree, milestones, estimates, current focus |
| `docs/`: method, sessions, tutor commands, setup, the spec for personal docs | `BASELINE.md`: starting level and the evidence for it |
| `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/`, `.gemini/`: tutor rules, skills, agents for each tool | `log.csv`, `reviews.json` (redo schedule), `mistakes.md`, `cheatsheet.md`, `weekly/`, `mocks/` |
| | `docs/`: your own docs, written by the tutor (`PERSONAL_DOCS.md`): pitfalls, weekly rhythm, interview prep and work habits when relevant |
| | `workspace/<track>/<module>/`: your attempts, `.history/` with earlier attempts, `primm/` with lesson files |

Back up or move personal data with `python dojo.py export` (a zip), optionally straight to
another machine over SSH with `--to user@host:path`, and restore it with `python dojo.py import`.

## Starting as a new learner

1. `python dojo.py setup` in a terminal (it installs, asks, checks and says what comes next),
   or say "set me up" to the tutor, which asks in the chat and runs it for you.
2. Say `assess me` (the tutor goes on to it by itself after "set me up"). The tutor asks about
   your background and goals, imports what you already have (notes, old logs, a list of topics
   you know), gives a short diagnostic, and then writes your `BASELINE.md`, `PLAN.md` and
   personal docs, sets your start module and seeds the redo queue for what you already know.
3. Follow `docs/DAILY_SESSION.md`. Re-run `/dojo-assess` monthly, or whenever the plan feels
   wrong.

## Skill trees

A plan organises skills in rings: inner rings first, and an outer ring unlocks when the gate
of the ring it depends on is met. The rings are built from the learner's goals, not from a fixed
template: each ring serves a goal they stated, in their priority order, after its prerequisites
(`ROADMAP.md`). Their number varies, and nothing the learner wants is labelled optional; only an
idea they called "maybe" is marked as such. Two learners, two trees:

```
"Pass a Python interview; robotics later"      "Data analysis at work, then web back ends"
Ring 1  Python fundamentals                    Ring 1  Python fundamentals
Ring 2  algorithms + interview practice        Ring 2  files, SQL, pandas, a data project
Ring 3  C, then C++ basics (for ROS)           Ring 3  HTTP, a web framework, testing
Ring 4  ROS 2 and a robot project              Ring 4  (maybe) deployment and cloud
```

Each ring names the goal it serves, its tracks or modules, and the gate that unlocks the next.
The skill tree and the roadmap table in `PLAN.md` describe the same plan and change together.

Rules of thumb: one main track at a time, at most one taster of the next; measurable gates,
not feelings or dates, decide when to move on. The full rules for ordering and mixing tracks,
and when the plan changes, are in `ROADMAP.md`; `python dojo.py mix` records the shares.

## Adding a track

1. Create `tracks/<name>/track.json`:

```json
{
  "name": "Rust",
  "description": "Ownership, borrowing, traits, then systems projects.",
  "extension": ".rs",
  "test_file": "tests/test_{slug}.rs",
  "solution_file": ".solutions/{slug}.rs",
  "clarify_file": ".clarify/{slug}.md",
  "test_command": ["cargo", "test", "--quiet", "--manifest-path", "{track_dir}/Cargo.toml", "{slug}"],
  "requires": ["Fluent in one language (first milestone of its track)"]
}
```

   `test_command` placeholders: `{python}` (the venv's Python), `{test}`, `{source}` (the file
   under test: the learner's attempt, the reference solution or the stub), `{slug}`, `{root}`,
   `{track_dir}`. The same path is also in the environment variable `DOJO_SOURCE`, and
   `DOJO_TARGET` is `solution` or `stub` during verification. A command that exits with 0
   means "passed". Set `"test_command": null` for a track without automatic tests (a reading
   or theory track); attempts are then logged by hand and judged with the tutor.

   `requires` (optional) lists, in words, what a learner should have before starting the track;
   the roadmap reads it (`ROADMAP.md`).

2. Write `tracks/<name>/README.md`: the phases, the modules with one focus line each,
   measurable milestones (copy the structure of `tracks/python/README.md`), a "Prerequisites"
   section and a "Theory" section (the background the track relies on, by module). No time
   estimates: they depend on the learner and live in their `PLAN.md`.

3. Add modules as folders (`m01_basics/`, ...) with exercises in the format below. Ask the
   tutor (`/dojo-new-exercise`) to generate them; it verifies each one.

4. Add the track to your profile (`python dojo.py mix <track>=N ...`, or ask the tutor to plan
   it with you: `plan my learning`) and to your `PLAN.md`.

## Exercise format

```text
<track>/<module>/
  e01_<slug>.<ext>           task + stub. e = write, b = fix a bug, r = read and predict
  tests/test_<slug>.<ext>    tests (path set by "test_file")
  .solutions/<slug>.<ext>    reference solution (path set by "solution_file")
  .clarify/<slug>.md         Pattern: line + the interviewer's answers on edge cases ("clarify_file")
  primm/README.md            the concepts a teach-me lesson can cover in this module, and an
                             optional "Theory:" line (background offered before the module)
```

The learner's side mirrors it: `workspace/<track>/<module>/` holds their attempts,
`.history/` (earlier attempts, moved there when a redo starts) and `primm/` (the files they type
in a lesson; `python dojo.py primm <module> <topic>` creates it). The tracker ignores
`primm/` folders, so lesson files never count as exercises. Every new module gets a
`primm/README.md` listing its concepts, plus a `Theory:` line when the module relies on
background that is not code (complexity, memory, maths); the tutor offers it before the
module's first exercise (`ROADMAP.md`, section 6).

- `<slug>` is unique across all tracks (it is the exercise's name in the tracker).
- The task text contains these header lines (in a docstring or comments):
  `Level: tiny|easy|medium|hard`, `Target: <minutes>`, and optionally `Kind: debug|predict`.
- The task gives the statement, ONE main example, ONE `Trace by hand:` input printed WITHOUT its
  output (a different, ordinary input of 4 to 6 items that goes through the main path; never an
  edge case, which the learner finds; write exercises only, since a `b` or `r` task is itself the
  trace; a `b` task instead shows a `Check your fix with:` input, printed without its output,
  that varies a parameter from the example so a fix that only repairs the example fails), and any constraint an interviewer would state
  up front ("do not use max()", "aim for O(n)"), including the contract: return a new
  object or change the input in place. No edge cases, no tips, no pattern name:
  discovering those is the learner's job. They go in `.clarify/<slug>.md`, which starts with a
  `Pattern: <short-name>` line (read by the tracker, hidden from the learner until `done`),
  followed by the answers to the clarifying questions an interviewer would expect.
- Targets: tiny 5, easy 10 to 15, medium 20 to 30, hard 45 minutes, for a learner at the
  module's level working alone.
- Each exercise has 3 to 6 tests, including edge cases. `python dojo.py verify` must show that
  the stub fails and the reference passes.
- Good exercises use a different story from the concept's worked example, have one clear
  pattern, and name their edge cases in the task.
