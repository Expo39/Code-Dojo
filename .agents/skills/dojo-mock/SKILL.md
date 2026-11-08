---
name: dojo-mock
description: Run a realistic live-coding mock interview or a single timed interview problem for the Code Dojo learner, then give scored feedback and log it. Use when the learner says "mock interview", "interview problem", "practice interview", or on mock day (its frequency follows the learner's mode, docs/METHOD.md).
---

# Mock interview

Behave like a real interviewer: friendly, mostly quiet, answering clarifying questions honestly. The learner writes everything.

## Setup

- Ask: full mock (45 to 60 minutes: 5 minutes of "tell me about yourself", one or two problems, 5 minutes of their questions) or a single timed problem (20 to 30 minutes)? Ask for a difficulty if they have a preference; otherwise choose from `progress/PLAN.md` and `dojo.py stats` (just above their comfortable level). If `progress/docs/INTERVIEW_PREP.md` names a company standard, match its format and level.
- Choose an UNSEEN problem in the track's language. Vary the type across mocks: classic pattern problems, practical ones (parse and aggregate a log, a small class with state, a validation function), "find the bug in this code", and "explain what this code does". Do not reuse problems from `tracks/` or past mocks in `progress/mocks/`.
- Wait for their "go" before writing the files or showing the problem (`AGENTS.md`: everything waits for their go).
- **Set up the files as an interview platform would** (CoderPad, HackerRank, a shared editor with a starter file): never a blank file. In `workspace/<track>/mocks/<type>/`, the problem's type: `pattern` (a classic pattern problem), `practical` (parse and aggregate, a small class with state, validation), `bug` (find the bug), `explain` (explain this code). Create the folders; these are your files, not the learner's code. `<problem>` is the problem's focus in snake_case (`popular_items`), and the file name adds the date:
  - `<problem>_<DD_MM_YYYY><ext>` (underscores, so a test can import it; a name already taken gets `_2`): a docstring or comment block with the full problem statement, the input and output types, constraints, and one or two examples with their outputs; then the signature with an empty body (`raise NotImplementedError` in Python; the track's equivalent elsewhere). For a small class with state: the class with its method signatures and one-line docstrings. For "find the bug": the buggy code. For "explain this code": the code only.
  - its test file at the track's `test_file` pattern inside the type folder (`mocks/<type>/tests/test_<problem>_<DD_MM_YYYY>.py` in Python: only the starter files sit in `mocks/<type>/`): the visible sample tests, exactly the docstring examples and nothing more, in the track's test style; a Python test adds the folder above it (`Path(__file__).parent.parent`) to `sys.path` before importing. Check they fail against the stub. "Explain this code" has no test file.
  - Copy the untouched starter file to `mocks/<type>/.history/<problem>_<DD_MM_YYYY>_original<ext>`, so their final code can be compared with it afterwards.
  - The hidden cases (edge cases, a second shape of input) stay with you, in your scratchpad, never in `workspace/`; they are what the learner's clarifying questions would uncover. They go into the report afterwards.
  - Run `dojo.py start <problem>_<DD_MM_YYYY>`. Give the file path and the problem statement in the chat as well.

## During

- Give the problem statement only. Answer clarifying questions. Do not volunteer edge cases.
- If they are silent for long, prompt once: "Can you talk me through what you are thinking?"
- If stuck for more than about 5 minutes: one small hint, as an interviewer would, and count it.
- They may run the sample tests at any point: prediction first, then the run command in its own message (the track's test command on that file, e.g. `.venv/bin/python -m pytest -q workspace/python/mocks/<type>/tests/test_<problem>_<DD_MM_YYYY>.py`). Passing samples is not "done", as on a real platform.
- When they say they are done, run their code on the samples and your hidden cases and show a table (input, got, expected). A failing hidden case is theirs to read and fix, as an interviewer would ask.

## Feedback (after time is up)

Score 1 to 4 on each, with one concrete example from the session for each score:

| Area | What 4 looks like |
| --- | --- |
| Understanding | Restated the problem, asked about edge cases before coding |
| Approach | Stated a plan and its complexity before typing; started simple |
| Code | Correct, clear names, no hard-coded example values, parse-then-act |
| Testing | Traced the example, tried an edge case, found and fixed own bugs |
| Communication | Talked throughout; calm when stuck |

Also list which exercise-loop steps (`docs/CHECKLISTS.md`) were skipped, and pass them with `--skipped` when logging.

Result: `strong` (mostly 4s), `pass` (no score below 3 and the problem solved), or `fail`.

## Log

- `dojo.py done <problem>_<DD_MM_YYYY> --kind mock --result <strong|pass|fail> --hints N --target <planned minutes> --level <level> --pattern <pattern> --no-review --note "<one line>"`. The fluency gate in `stats` reads these results.
- Write `progress/mocks/<DD-MM-YYYY>_<problem>.md`: the problem, their final code (copied from their file), the hidden cases with their results, the scores with examples, the 2 habits to work on, and a similar problem to practise. If `progress/docs/INTERVIEW_PREP.md` exists, update its "habits from the latest mock" line.
- Log mistakes with `dojo.py mistake`. If it went badly, offer the similar problem as a `dojo-new-exercise` so it enters the redo queue.
