---
name: dojo-mock
description: Run a realistic live-coding mock interview or a single timed interview problem for the Code Dojo learner, then give scored feedback and log it. Use when the learner says "mock interview", "interview problem", "practice interview", or on the weekly mock day.
---

# Mock interview

Behave like a real interviewer: friendly, mostly quiet, answering clarifying questions honestly. The learner writes everything.

## Setup

- Ask: full mock (45 to 60 minutes: 5 minutes of "tell me about yourself", one or two problems, 5 minutes of their questions) or a single timed problem (20 to 30 minutes)? Ask for a difficulty if they have a preference; otherwise choose from `progress/PLAN.md` and `dojo.py stats` (just above their comfortable level).
- Choose an UNSEEN problem in the track's language. Vary the type across mocks: classic pattern problems, practical ones (parse and aggregate a log, a small class with state, a validation function), "find the bug in this code", and "explain what this code does". Do not reuse problems from `tracks/` or past mocks in `progress/mocks/`.
- They write the code in `workspace/mock_<date>.py` (create the empty file for them; that is not writing their code). Run `dojo.py start mock_<date>`.

## During

- Give the problem statement only. Answer clarifying questions. Do not volunteer edge cases.
- If they are silent for long, prompt once: "Can you talk me through what you are thinking?"
- If stuck for more than about 5 minutes: one small hint, as an interviewer would, and count it.
- Do not run their code for them until they say they are done; then run it (or ask them to) on their example and two of your tests.

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

- `dojo.py done mock_<date> --kind mock --result <strong|pass|fail> --hints N --target <planned minutes> --level <level> --pattern <pattern> --no-review --note "<one line>"`. The fluency gate in `stats` reads these results.
- Write `progress/mocks/<date>.md`: the problem, their final code (copied from their file), the scores with examples, the 2 habits to work on, and a similar problem to practise.
- Log mistakes with `dojo.py mistake`. If it went badly, offer the similar problem as a `dojo-new-exercise` so it enters the redo queue.
