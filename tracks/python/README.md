# Python track

Python fundamentals, reading and debugging code, then data structures and algorithms, with
projects and interview practice throughout. One of the tracks a learner can choose; nothing
here is compulsory. A learner's own goals and dates live in their `progress/PLAN.md`.

Python is a good first language for this because its syntax gets out of the way, so the time
goes into thinking, reading and debugging, and because it is the most common language in
live-coding interviews.

| Stage | Covers | Done when |
| --- | --- | --- |
| Phase 1: Foundations | writing, reading and debugging everyday Python | gate M1 |
| Phase 2: Patterns and engineering | data structures, algorithms, testing, projects | progress towards M2 |
| Phase 3: Interview strength | unseen mediums under time pressure, mocks | gate M2 |

No durations here: how long a phase takes depends on the learner's hours, speed and hints, so
estimates live in each learner's `progress/PLAN.md`, made from their own log and revised as it
grows (`docs/ROADMAP.md`).

## How exercises work here

```text
tracks/python/m04_parsing/
  e01_parse_pairs.py            the task (docstring) and a stub: never edited
  tests/test_parse_pairs.py     the tests
  .solutions/parse_pairs.py     reference answer: the tutor reads it for hints, you do not
  .clarify/parse_pairs.md       the interviewer's answers on edge cases (python dojo.py clarify)
  primm/README.md               the concepts a `teach me` lesson covers in this module
```

Your side mirrors it, one folder per module (personal, gitignored):

```text
workspace/python/m04_parsing/
  parse_pairs.py                your attempt
  .history/                     earlier attempts, moved here when a redo starts
  primm/<topic>.py              what you type during a teach-me lesson
```

`python dojo.py start parse_pairs` copies the stub to `workspace/python/m04_parsing/parse_pairs.py`
(your file) and starts the timer; `python dojo.py test parse_pairs` runs the tests against your file;
`python dojo.py done parse_pairs --hints N` logs the attempt and schedules the next redo.
Prefixes: `e` = write it, `b` = find and fix the bug, `r` = read and predict.

## Phases and modules

The order is the same for everyone; the pace is personal. Gates, not dates, decide when a phase
is done (`python dojo.py stats`).

### Phase 1: Foundations

| Module | Focus | Status |
| --- | --- | --- |
| m01_foundations | loops, conditions, accumulators, best-so-far, range, enumerate, return | seeded |
| m02_strings_lists | slicing, split/join, zip, comprehensions, runs | seeded |
| m03_dicts_sets | counting, grouping, seen-sets, set operations | seeded |
| m04_parsing | text to records, logs, config, CSV, parse-then-act | seeded |
| m05_functions_errors | sort keys, try/except, raising, default arguments, closures, higher-order functions | seeded |
| m06_classes | state, custom exceptions, dunder methods, dataclasses, inheritance | seeded |
| m07_debugging | classic logic bugs, found with the debugger | seeded |
| m08_python_model | names vs objects, mutability, aliasing, copies, scope, late binding | seeded |
| m09_iterators_decorators | generators, decorators, context managers, recursion | seeded |
| m10_reading_code | tracing by hand, predicting output | seeded |
| m11_files_stdlib | files, pathlib, json, datetime, collections | seeded |
| m12_testing | writing your own tests: pytest, parametrize, raises, fixtures, edge cases | planned |
| Projects | P1 word-stats CLI, P2 todo app with JSON storage, P3 log analyser | `tracks/python/projects` |

### Phase 2: Patterns and engineering

| Module | Focus | Status |
| --- | --- | --- |
| m21_hashing | complexity basics, hash maps and sets | seeded |
| m22_two_pointers | sorted arrays, in-place, palindromes | seeded |
| m23_sliding_window | fixed and variable windows | seeded |
| m24_stacks_queues | stack, queue, deque, monotonic stack | seeded |
| m25_binary_search | on arrays and on the answer | seeded |
| m26_recursion_backtracking | subsets, permutations, combinations | planned |
| m27_linked_lists | node classes, reversal, fast and slow pointers | planned |
| m28_trees | traversals, BST, depth, level order | planned |
| m29_graphs | grids, BFS, DFS, topological sort | planned |
| m30_heaps | heapq, top k, merging | planned |
| m31_intervals_greedy | sorting by key, merging intervals, greedy choices | planned |
| m32_dynamic_programming | 1-D DP, memoisation, classic problems | planned |
| m33_practical | LRU cache, TTL cache, event scheduler, small design problems | planned |
| Projects | P4 text adventure (state machine), P5 inventory/bank system with tests and persistence, P6 an HTTP API client | `tracks/python/projects` |

"Planned" modules are generated when you reach them (`/dojo-new-exercise`, or ask the tutor),
using the module's focus line above. External problem lists (NeetCode 150 and LeetCode) fill in
alongside; log those with `python dojo.py done <name> --minutes N --hints H --level easy --pattern <p>`.

### Phase 3: Interview strength and polish

Mixed mediums under time pressure, frequent mocks (if interviews are a goal), practical problems (parse and aggregate,
small class design, debugging an unfamiliar codebase), and explaining your projects. Python
becomes the language you think in.

### After M2

Keep Python sharp in maintenance (`python dojo.py mix python=0 ...`: the redo queue keeps coming,
plus a regular mock) and choose what comes next with the tutor (`plan my learning`,
`docs/ROADMAP.md`): go deeper in Python (web back ends, data, automation) or add another track.

---

## Milestones and fluency gates

`python dojo.py stats` checks the measurable gates automatically from your log. They are
options, not a ladder everyone must climb: a learner's plan picks the bar that is enough for
their goal (`docs/ROADMAP.md`), which may be M1, a practical-round bar, or more, and drops the
track to maintenance once it is met.

| Milestone | Meaning | Gate |
| --- | --- | --- |
| **M1 Fundamentals fluent** | You can write everyday Python from a blank file without lookups | Phase 1 modules attempted; last 10 easy problems all solved, median at or under 1.2x target, at most 0.5 hints on average; projects P1 and P2 done; can explain mutability, scope and generators out loud |
| **M2 Interview-ready** | You would pass most junior and mid-level live-coding rounds | Last 10 easy at or under 1.0x with 0 hints; last 8 mediums solved at or under 1.3x with at most 1 hint; last 3 mocks passed; P3 to P5 done |
| **M3 Strong** | You are the person who explains the bug to others | About 150 unique problems solved, most patterns at box 4 (mastered); mediums at or under target; can review AI code and find its bugs reliably |

Mocks are logged with `python dojo.py log mock 60 --result pass` (or `fail` / `strong`).

## How the plan adapts

- **Behind on time this week?** `today` shows the gap and a capped catch-up (at most an extra
  hour a day). A short week is normal; the plan stretches, it does not punish.
- **Slow or hint-heavy on a pattern?** It shows under "Weak spots" in `today` and in the
  weekly report; the weekly review turns it into a `teach me` lesson plus redos before any new
  material.
- **Faster than planned?** Skip ahead (`python dojo.py settings start_module=<module>`), or mark
  known material with `python dojo.py mark <module> --box 2`. `/dojo-assess` does this properly.
- **Training different hours than planned?** The weekly review suggests settings that match
  what you really do, one yes-or-no question each.

## Engineer skills trained throughout

Not a phase: they run through every week.

| Skill | How the dojo trains it |
| --- | --- |
| Reading and understanding code | predict drills, `m10_reading_code`, review drills on AI-written code, reading real open-source and standard-library code |
| Debugging | `m07`, `m08`, bug drills, always confirming a hypothesis in the debugger before fixing |
| Testing | every exercise has tests; from Phase 2 you write the tests yourself (`m12`, projects) |
| Communication | talk-aloud solving, explain drills, mock interviews (as often as your mode says), explaining your projects |
| Working with AI critically | the tutor never writes your code; review drills train spotting plausible-but-wrong code; in projects you may use AI only to *explain*, then you verify |
| Tools | terminal, git, a debugger, a virtual environment, pytest |


## Resources for this track

| Need | Resource |
| --- | --- |
| The language, properly | Python tutorial: https://docs.python.org/3/tutorial/ |
| How names and objects really work | Ned Batchelder, "Facts and myths about Python names and values": https://nedbatchelder.com/text/names.html |
| Cost of operations | https://wiki.python.org/moin/TimeComplexity |
| Standard library | `collections`, `itertools`, `functools`, `pathlib`, `json`, `datetime`: https://docs.python.org/3/library/ |
| Small idiomatic exercises with mentoring | Exercism Python: https://exercism.org/tracks/python |
| Patterns, in order, with videos when stuck | NeetCode roadmap: https://neetcode.io/roadmap |
| Interview problems | LeetCode Top Interview 150: https://leetcode.com/studyplan/top-interview-150/ |
| Practising out loud with a person | Pramp or interviewing.io, or a friend reading you a problem |
| Testing | pytest docs, "Get started" and "How to parametrize": https://docs.pytest.org/ |
