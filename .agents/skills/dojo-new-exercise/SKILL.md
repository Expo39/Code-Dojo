---
name: dojo-new-exercise
description: Create new verified Code Dojo exercises. Use when the learner says "new exercise on <topic>", "more like <exercise>", "from scratch <topic>", when a planned module from a track README is reached, or when a weak spot needs more practice.
---

# New exercises

1. Judge first: could an existing exercise train this with a small change, or one exercise cover two topics? Prefer that over adding (`dojo-new-track`, step 6). Then decide the spec: track, module (existing, or the next planned one in `tracks/<track>/README.md`), topic and pattern, level and target time, how many (usually 2 to 5), and the learner's weak spots to target (`progress/mistakes.md`, `dojo.py stats`). "More like X" keeps X's pattern in a different story with slightly different edge cases.
2. Delegate the writing to the `problem-setter` agent with that spec and the path of one existing exercise in the same track as a format example. Ask it to run `dojo.py verify <slugs>` and fix until it passes.
3. Check its report: the slugs, `verify` passing, and that the task text does not leak the solution. Do not show the learner the reference solutions.
4. Exercises made at this learner's request: run `dojo.py changes --ack <slugs>`, so they are not asked about them. Exercises added to the shared track for everyone (a track review): do not acknowledge them; learners who started that module are asked at their next session, the others meet them there. Tell the learner the new exercise names and the first command: `dojo.py start <slug>`; start it only on their "go".

A brand-new module also needs its focus line marked as "seeded" in the track README (status column) and a `primm/README.md` with its concepts and, when the module relies on background theory, a `Theory:` line (the problem-setter adds it).
