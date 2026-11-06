---
name: dojo-drill
description: Short drills for reading, debugging and explaining code in the Code Dojo. Use when the learner says "bug drill", "predict drill", "trace drill", "review drill", or "explain drill".
---

# Drills

Always NEW material, written for the drill: never reuse exercise files or reveal anything from `.solutions/`. Match the learner's current level (`progress/PLAN.md`) and target their recurring mistakes (`progress/BASELINE.md`, `progress/mistakes.md`). Log each drill: `dojo.py log drill <minutes> <type> --result <right|wrong>`; log wrong answers with `dojo.py mistake`.

## predict drill

Ask for the prediction and wait; give the run command only in the next message, never in the same one.
Show a 5 to 12 line snippet (a language gotcha or a small algorithm). Ask what it prints (`docs/PITFALLS.md` lists the classic traps to draw from). After their answer, reveal and explain, and name the concept. Do 3 in a row unless asked otherwise.

## trace drill
A 10 to 20 line function and one input. The learner writes the value of each variable after each loop iteration (a trace table). Check the table row by row.

## bug drill
Write a 5 to 15 line function with ONE realistic bug, plus a failing test, in the track's language (extension and test style from `tracks/<track>/track.json`), to `workspace/drills/bug_<n><ext>` and a matching test file (create `workspace/drills/` if needed; these are your files, so writing them is allowed). The learner predicts the bug before running anything, confirms it in the debugger, and fixes it with the smallest change. Never reveal the bug before they find it; hints follow the ladder.

## review drill
Show 15 to 40 lines of code with several problems (correctness, edge cases, security, performance, readability). Often present it as "an AI assistant wrote this; would you merge it?" The learner lists every problem; then score their list against yours (found / missed / false alarms) and explain the misses. This trains the most important AI-age skill: catching plausible-but-wrong code.

## explain drill: work (optional)
The learner explains, from memory, a part of their current work project they only partly understand: what it does, inputs and outputs, edge cases, why it is written that way. Do NOT ask for or accept pasted work code; work only from their explanation. Ask the follow-up questions a senior colleague or interviewer would ask, list the gaps to look up, and log `dojo.py log drill 20 work-explain`. See `progress/WORK_HABITS.md` if it exists.

## explain drill
Give a task and ask them to answer WITHOUT code, using the five steps in `docs/INTERVIEW_PLAYBOOK.md` ("When you cannot write something"): concept and approach, skeleton, the precise thing to look up, how to verify, trade-offs. Score each step out of 2 and say what was missing.
