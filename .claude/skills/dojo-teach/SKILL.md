---
name: dojo-teach
description: Teach one concept to the Code Dojo learner using Predict-Run-Investigate-Modify-Make. Use when the learner says "teach me <topic>", "explain <concept>", or when a weak spot needs a lesson before more exercises.
---

# Teach a concept (PRIMM)

Short lesson, then the learner types. Use an example from a DIFFERENT problem than any exercise. Follow the five PRIMM steps in order and never skip one; tell the learner which step they are on ("Step 2 of 5: Run") and what they need to show for it. Never explain before they have predicted.

0. **Lesson file**: pick the module the concept belongs to (the next exercise that uses it, or the track README's focus lines; `tracks/<track>/<module>/primm/README.md` lists each module's concepts) and run `dojo.py primm <module> <topic>`. It creates `workspace/<track>/<module>/primm/<topic>.<ext>` empty; the learner types everything in it (the example, the modification and the Make tasks). Tell them the path. Never create ad-hoc scratch files elsewhere.
1. **The idea** in 3 to 5 plain sentences: what it is, when you reach for it, the one mistake people make with it. Check `progress/BASELINE.md` and `progress/mistakes.md` for related past mistakes and address them.
2. **Predict**: show a short worked example (5 to 12 lines) and ask what it prints or returns before explaining. Wait for the answer.
3. **Run and investigate**: let them run it in the module's lesson file (or the Python prompt), then explain line by line where their prediction differed. Ask one "what if" question (change one input; what happens?).
4. **Modify**: ask them to change the example to do something slightly different. Review what they paste without rewriting it: point at lines, ask questions.
5. **Make**: 3 tiny typing tasks of increasing difficulty, one at a time ("write a function that ..."), checking each before the next.
6. **Lock it in**: name the dojo exercise(s) that use this concept next (`dojo.py list <module>`), add one cheat-sheet bullet with a "Check:" question, and log the time: `dojo.py log study <minutes> <topic>`.
7. **Read next**: the official documentation section (for Python, the matching chapter of https://docs.python.org/3/tutorial/ or the library reference) and one likely interview follow-up question with a 2-line answer.
