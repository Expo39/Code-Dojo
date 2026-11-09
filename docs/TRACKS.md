# Tracks, plans and adding your own

Code Dojo is a training system, not a fixed course. **Everything is optional.** A learner
chooses one or more *tracks* (subjects), and keeps a personal *plan* with their own goals,
skill tree and dates. The repo ships with a Python track as a complete example; anyone can add
a track for any subject (another language, a framework, maths, even a non-coding skill).

## What is shared and what is personal

| Shared (in git, the same for everyone) | Personal (in `progress/` and `workspace/`, gitignored, never pushed) |
| --- | --- |
| `dojo.py` and `dojolib/` (tracker), `conftest.py` | `profile.json`: name, mode, target level, time per day, rest days, target date, level, tracks, mix (`python dojo.py settings` shows it) |
| `tracks/<track>/`: syllabus, exercises, tests, reference solutions, `graph.json` (the concept graph) | `PLAN.md`: goals, roadmap (track order and mix), skill tree, milestones, estimates, current focus |
| `docs/`: method, sessions, tutor commands, setup, the spec for personal docs | `BASELINE.md`: starting level and the evidence for it |
| `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/`, `.gemini/`: tutor rules, skills, agents for each tool | `log.csv`, `reviews.json` (redo schedule), `graph.json` (your evidence per concept), shared `mistakes.md` and `cheatsheet.md`, `weekly/`; per track `<track>/` with its own notes and its `drills/`, `mocks/` and `probes/` reports (layout: `PERSONAL_DOCS.md`) |
| | `docs/`: your own docs, written by the tutor (`PERSONAL_DOCS.md`): pitfalls, weekly rhythm, interview prep and work habits when relevant |
| | `workspace/<track>/`: everything you type for that track: `<module>/` (attempts, `.history/` with earlier attempts, `primm/` with lesson files), `drills/<type>/`, `mocks/<type>/`, `projects/` |

Back up or move personal data with `python dojo.py export`: one zip with `progress/` and
`workspace/` (concept evidence and probe reports included) and, inside the same zip, `views/`
with `concept_graph.html` (every view in one page: open it in a browser) and a Mermaid file per view. Send it straight to
another machine over SSH with `--to user@host:path`, and restore it with `python dojo.py import`
(it restores the data; the views are always made fresh).

## Starting as a new learner

1. `python dojo.py setup` in a terminal (it installs, asks, checks and says what comes next),
   or say "set me up" to the tutor, which asks in the chat and runs it for you.
2. Say `assess me` (the tutor goes on to it by itself after "set me up"). The tutor asks about
   your background and goals, imports what you already have (notes, old logs, a list of topics
   you know), runs a short probe (what you want to be able to do, then the edge of what you hold
   on the track's concept graph), a short practical check, and then writes your `BASELINE.md`, `PLAN.md` and
   personal docs, sets your start module and seeds the redo queue for what you already know.
   Then you go through your modules together (`python dojo.py modules`): leave any out or add
   any back, each with a reason, and decide together.
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

## Concept graph

A track's `graph.json` maps what it teaches: one entry per concept, with what it needs first.
The skill tree in `PLAN.md` stays the plan (which goals, in what order); the graph is the map of
one subject that the plan, the probe, lessons and drills read. `python dojo.py graph` shows
everything you know as one graph (every track's concepts together), `graph <track>` one track,
each with your state on each concept; `graph next` ranks what you can do now; `graph path <goal>` lists the
fewest concepts still to learn to reach a goal; `graph --html` builds the interactive page and opens it
(`concept_graph.html` in the system's temporary folder, or `--out <folder>`; every export zip
carries one too): Map and Flow layouts, drag, zoom, search, focus on a neighbourhood, the path to
a concept, and a panel per concept (README, "See what you know").

```json
{"version": 1, "track": "python", "concepts": [
  {"id": "counting_dict", "name": "Counting with a dict", "module": "m03_dicts_sets",
   "kind": "skill", "requires": ["dict_basics", "accumulator"],
   "can": "Can predict the result of a loop that does d[k] = d.get(k, 0) + 1 over a list",
   "lesson": "counting", "exercises": ["word_count", "most_common_char", "merge_counts"]}
]}
```

| Field | Meaning |
| --- | --- |
| `id` | lower_snake_case, unique in the track |
| `module` | the module folder that teaches it |
| `kind` | `skill`, or `theory` for background from a `Theory:` line (its lesson is named after the id, `theory_<topic>`) |
| `requires` | concepts that must be held first; no cycles |
| `can` | what someone who holds it can do, observable: the probe and lessons test exactly this |
| `lesson` | a topic from the module's `primm/README.md` (optional) |
| `aliases` | other names a logged lesson may have used (optional) |
| `exercises` | the exercises that practise it (optional) |
| `planned` | `true` for a concept of a module not built yet |
| `shared` | `true` for a concept that holds in any language (Big-O, recursion, two pointers, BFS): another track's graph uses the same `id` and the same `can` statement, the combined graph shows it once, and evidence from any track counts for all of them. Language rules (how Python slices, what `std::vector` does) are never shared |

Your state on each concept is computed, never typed: from your log (a solved exercise, a lesson,
a mock with its pattern), your redo boxes, and evidence the tutor records after a probe or a
lesson (`graph set`). The states:

| State | Meaning |
| --- | --- |
| fluent | every exercise of it is in box 2 or higher |
| held | understood: a lesson or a clean solve, or implied because something built on it is solid |
| due | held, with a redo of one of its exercises due |
| fragile | a struggle or a probe answer right but unsure |
| misconception | a wrong answer given with confidence; repaired before anything builds on it |
| gap | not known yet (a probe miss or "I don't know") |
| ready | not met yet, and everything it needs is solid: something you can start now |

`python dojo.py graph check` validates a graph (ids, links to modules, lessons and exercises, no
cycles, shared concepts that agree across tracks); `doctor` and the pre-push checks run it.

## Adding a track

Start with research, not a blank page: say "design a track for <subject>" (skill
`dojo-new-track`). It surveys the best free material (university courses such as MIT, Stanford,
Harvard, Helsinki and Oxford, official documentation, well-regarded repositories on GitHub,
GitLab and Codeberg, free books), judges each source on authority, currency, depth, exercises
and licence (stars and "free" are not proof of quality, and niche topics need extra care).
The aim is the best possible course, not a copy of the free ones: the strongest sources are the
starting point, and the tutor's own judgement fills their gaps (what they miss, teach badly or
leave without practice). Exercises are always original. The steps below are what it produces; you can also follow them by hand.

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
  "requires": ["Fluent in one language (first milestone of its track)"],
  "reviewed": "07/11/2026"
}
```

   `test_command` placeholders: `{python}` (the venv's Python), `{test}`, `{source}` (the file
   under test: the learner's attempt, the reference solution or the stub), `{slug}`, `{root}`,
   `{track_dir}`. The same path is also in the environment variable `DOJO_SOURCE`, and
   `DOJO_TARGET` is `solution` or `stub` during verification. A command that exits with 0
   means "passed". Set `"test_command": null` for a track without automatic tests (a reading
   or theory track); attempts are then logged by hand and judged with the tutor.

   `requires` (optional) lists, in words, what a learner should have before starting the track;
   the roadmap reads it (`ROADMAP.md`). `reviewed` is the date the track was last checked
   against current courses and the current version; `doctor` flags a track not reviewed for
   over a year, because the field keeps changing.

2. Write `tracks/<name>/README.md`: the phases, the modules with one focus line each,
   measurable milestones (copy the structure of `tracks/python/README.md`), a "Prerequisites"
   section and a "Theory" section (the background the track relies on, by module), a "Last
   reviewed: <date>, against <tool and version>" line at the top, and a sources table (what each
   source was used for, why it is trusted). No time estimates: they depend on the learner and
   live in their `PLAN.md`.

3. Add modules as folders (`m01_basics/`, ...) with exercises in the format below. Ask the
   tutor (`/dojo-new-exercise`) to generate them; it verifies each one.

4. Write `tracks/<name>/graph.json` (see "Concept graph"): every concept the modules teach,
   with each exercise listed under the concept it trains, and run `python dojo.py graph check
   <name>`.

5. Add the track to your profile (`python dojo.py mix <track>=N ...`, or ask the tutor to plan
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
in a lesson; `python dojo.py primm <module> <topic>` creates it). Drills, mock code and projects
sit beside the modules in `workspace/<track>/drills/`, `mocks/` and `projects/`, so each track's
code stays in one folder. Drills and mocks sit in type folders (`drills/bug/`, `drills/review/`,
`mocks/practical/`, ...), each with its own test folder and `.history/` where the kind needs them
(bug drills and mocks; review drills are only the file), and each file is named
after its focus (`drills/bug/find_owner.py`, `mocks/practical/popular_items_07_11_2026.py`), so
they stay easy to find as they pile up. The tracker moves older layouts (the root `drills/` and
`mocks/`, numbered `bug_<n>` and `mock_<date>` files) into this one. The tracker ignores
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
