---
name: dojo-new-exercise
description: Create new verified Code Dojo exercises. Use when the learner says "new exercise on <topic>", "more like <exercise>", "from scratch <topic>", when a planned module from a track README is reached, or when a weak spot needs more practice.
---

# New exercises

1. Decide the spec: track, module (existing, or the next planned one in `tracks/<track>/README.md`), topic and pattern, level and target time, how many (usually 2 to 5), and the learner's weak spots to target (`progress/mistakes.md`, `dojo.py stats`). "More like X" keeps X's pattern in a different story with slightly different edge cases.
2. Delegate the writing to the `problem-setter` agent with that spec and the path of one existing exercise in the same track as a format example. Ask it to run `dojo.py verify <slugs>` and fix until it passes.
3. Check its report: the slugs, `verify` passing, and that the task text does not leak the solution. Do not show the learner the reference solutions.
4. Tell the learner the new exercise names and the first command: `dojo.py start <slug>`.

A brand-new module also needs its focus line marked as "seeded" in the track README (status column) and a `primm/README.md` with its concepts (the problem-setter adds it).
