# Tracks, plans and adding your own

Code Dojo is a training system, not a fixed course. **Everything is optional.** A learner
chooses one or more *tracks* (subjects), and keeps a personal *plan* with their own goals,
skill tree and dates. The repo ships with a Python track as a complete example; anyone can add
a track for any subject (another language, a framework, maths, even a non-coding skill).

## What is shared and what is personal

| Shared (in git, the same for everyone) | Personal (in `progress/` and `workspace/`, gitignored, never pushed) |
| --- | --- |
| `dojo.py` (tracker), `conftest.py` | `profile.json`: name, time per day, rest days, target date, level, tracks |
| `tracks/<track>/`: syllabus, exercises, tests, reference solutions | `PLAN.md`: goals, skill tree, milestones, estimates, current focus |
| `docs/`: method, sessions, tutor commands, setup | `BASELINE.md`: starting level and the evidence for it |
| `.claude/`: tutor rules, skills, agents | `log.csv`, `reviews.json` (redo schedule), `mistakes.md`, `cheatsheet.md`, `weekly/`, `mocks/` |
| | `WORK_HABITS.md` (optional): how training relates to your job |
| | `workspace/<track>/<module>/`: your attempts, `.history/` with earlier attempts, `primm/` with lesson files |

Back up or move personal data with `python dojo.py export` (a zip), optionally straight to
another machine over SSH with `--to user@host:path`, and restore it with `python dojo.py import`.

## Starting as a new learner

1. `python dojo.py install`, then `python dojo.py setup` (time, rest days, tracks, level).
2. In Claude Code, run `/dojo-assess`. The tutor asks about your background, imports what you
   already have (notes, old logs, a list of topics you know), gives a short diagnostic, and
   then writes your `BASELINE.md` and `PLAN.md`, sets your start module and seeds the redo
   queue for what you already know.
3. Follow `docs/DAILY_SESSION.md`. Re-run `/dojo-assess` monthly, or whenever the plan feels
   wrong.

## Skill trees

A plan organises skills in rings: inner rings first, outer rings unlock when the inner ring's
gate is met. Typical shape:

```
Ring 1  fundamentals of the first track     fluency: write, read, debug
Ring 2  depth: patterns + engineering        testing, design, projects
Ring 3  optional directions                  other tracks, chosen later, only if wanted
```

Rules of thumb: one main track at a time; at most 10% of a week on a "taster" of the next ring;
measurable gates, not feelings, decide when to move on.

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
  "test_command": ["cargo", "test", "--quiet", "--manifest-path", "{track_dir}/Cargo.toml", "{slug}"]
}
```

   `test_command` placeholders: `{python}` (the venv's Python), `{test}`, `{source}` (the file
   under test: the learner's attempt, the reference solution or the stub), `{slug}`, `{root}`,
   `{track_dir}`. The same path is also in the environment variable `DOJO_SOURCE`, and
   `DOJO_TARGET` is `solution` or `stub` during verification. A command that exits with 0
   means "passed". Set `"test_command": null` for a track without automatic tests (a reading
   or theory track); attempts are then logged by hand and judged with the tutor.

2. Write `tracks/<name>/README.md`: the phases, the modules with one focus line each, and
   measurable milestones (copy the structure of `tracks/python/README.md`).

3. Add modules as folders (`m01_basics/`, ...) with exercises in the format below. Ask the
   tutor (`/dojo-new-exercise`) to generate them; it verifies each one.

4. Add the track to your profile (`python dojo.py setup`) and to your `PLAN.md`.

## Exercise format

```text
<track>/<module>/
  e01_<slug>.<ext>           task + stub. e = write, b = fix a bug, r = read and predict
  tests/test_<slug>.<ext>    tests (path set by "test_file")
  .solutions/<slug>.<ext>    reference solution (path set by "solution_file")
  .clarify/<slug>.md         Pattern: line + the interviewer's answers on edge cases ("clarify_file")
  primm/README.md            the concepts a teach-me lesson can cover in this module
```

The learner's side mirrors it: `workspace/<track>/<module>/` holds their attempts,
`.history/` (earlier attempts, moved there when a redo starts) and `primm/` (the files they type
in a lesson; `python dojo.py primm <module> <topic>` creates it). The tracker ignores
`primm/` folders, so lesson files never count as exercises. Every new module gets a
`primm/README.md` listing its concepts.

- `<slug>` is unique across all tracks (it is the exercise's name in the tracker).
- The task text contains these header lines (in a docstring or comments):
  `Level: tiny|easy|medium|hard`, `Target: <minutes>`, and optionally `Kind: debug|predict`.
- The task gives the statement, ONE main example and any constraint an interviewer would state
  up front ("do not use max()", "aim for O(n)"). No edge cases, no tips, no pattern name:
  discovering those is the learner's job. They go in `.clarify/<slug>.md`, which starts with a
  `Pattern: <short-name>` line (read by the tracker, hidden from the learner until `done`),
  followed by the answers to the clarifying questions an interviewer would expect.
- Targets: tiny 5, easy 10 to 15, medium 20 to 30, hard 45 minutes, for a learner at the
  module's level working alone.
- Each exercise has 3 to 6 tests, including edge cases. `python dojo.py verify` must show that
  the stub fails and the reference passes.
- Good exercises use a different story from the concept's worked example, have one clear
  pattern, and name their edge cases in the task.
