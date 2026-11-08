---
name: dojo-drill
description: Short drills for reading, debugging and explaining code in the Code Dojo. Use when the learner says "bug drill", "predict drill", "trace drill", "review drill", or "explain drill".
---

# Drills

Wait for the learner's "go" before writing or showing a drill, even when the session template says a drill is next (`AGENTS.md`: everything waits for their go). A drill that needs files (code to review, a trace or predict snippet the learner keeps) follows the same layout in its own type folder: `workspace/<track>/drills/<type>/<focus><ext>` with that folder's tests and `.history/` (`AGENTS.md`, generated files). Always NEW material, written for the drill: never reuse exercise files or reveal anything from `.solutions/`. Match the learner's current level (`progress/PLAN.md`) and target their recurring mistakes (`progress/BASELINE.md`, `progress/mistakes.md`). Log each drill: `dojo.py log drill <minutes> <type> --result <right|wrong>`; log wrong answers with `dojo.py mistake`.

## Report (every drill with an answer)

After scoring, write `progress/drills/<DD-MM-YYYY>_<type>_<focus>.md` (a name already taken gets `_2`): a header (the drill file and its `.history/` original, the task in one line, the minutes), then
1. **My answer**: what the learner said, in their words, close to verbatim; for a second pass after a prompt, a separate list, saying what prompted it.
2. **The real issues** (or the right answers): a table with the line, the problem and why it is wrong, in words; never the fixed code.
3. **Comparison**: found on the first pass, found after a prompt, missed, false alarms (and any fair suggestion that is not a bug).
4. **The habit to take away**, one or two lines.
Predict and trace drills in chat get the same report (their predictions or table against the real values). The weekly review and the progress coach read these reports.

## predict drill

Ask for the prediction and wait; give the run command only in the next message, never in the same one.
Show a 5 to 12 line snippet (a language gotcha or a small algorithm). Ask what it prints (draw first from the learner's own traps in `progress/docs/PITFALLS.md` and recent rows of `progress/mistakes.md`). After their answer, reveal and explain, and name the concept. Do 3 in a row unless asked otherwise.

## trace drill
A 10 to 20 line function and one input. The learner writes the value of each variable after each loop iteration (a trace table). Check the table row by row.

## bug drill
Write a 5 to 15 line function with ONE realistic bug, plus a failing test, in the track's language (extension and test style from `tracks/<track>/track.json`), to `workspace/<track>/drills/bug/<focus><ext>`, where `<focus>` is the function's name in snake_case (`find_owner`; never a name that gives the bug away; a name already taken gets `_<DD_MM_YYYY>`), and its test file in the same type folder at the track's `test_file` pattern (`drills/bug/tests/test_<focus>.py` in Python; only the drill files sit in `drills/bug/`; create the folders if needed; these are your files, so writing them is allowed). The repo runs pytest with `--import-mode=importlib`, so a Python drill test adds the folder above it (`Path(__file__).parent.parent`) to `sys.path` before importing the drill; copy the untouched buggy file to `workspace/<track>/drills/bug/.history/<focus>_original<ext>` (never edited, so after the fix the learner compares the two with `diff`); check it fails before handing it over, and give the learner the run command (the track's test command on that file, e.g. `.venv/bin/python -m pytest -q workspace/python/drills/bug/tests/test_<focus>.py`; in the editor, "Debug: this file" runs it with breakpoints) only after their prediction. The docstring shows the main example AND a `Check your fix with:` input printed without its output, which varies a different parameter or shape from the example (another `k`, another length) so that a fix that only repairs the example fails on it; the learner traces it before and after the fix. The test file covers both. The learner predicts the bug before running anything, confirms it in the debugger, and fixes it with the smallest change. After the tests pass, give the comparison command (`! diff workspace/<track>/drills/bug/.history/<focus>_original<ext> workspace/<track>/drills/bug/<focus><ext>`) and ask them to say in one line what the fix changed and why. Never reveal the bug before they find it; hints follow the ladder.

## review drill
Show 15 to 40 lines of code with several problems (correctness, edge cases, security, performance, readability). Often present it as "an AI assistant wrote this; would you merge it?" The learner lists every problem; then score their list against yours (found / missed / false alarms) and explain the misses. This trains the most important AI-age skill: catching plausible-but-wrong code. Write it to `workspace/<track>/drills/review/<focus><ext>` with its untouched copy in `drills/review/.history/<focus>_original<ext>`. **Then the learner fixes it** (Modify): every issue on the agreed list, with the smallest changes, typed by them. Only now write the tests (the track's `test_file` pattern in `drills/review/`), one per issue plus the docstring example, so they never reveal an issue before the review; check they fail against the original. The learner predicts, then runs them (the command in its own message). After they pass, give the comparison command (`! diff workspace/<track>/drills/review/.history/<focus>_original<ext> workspace/<track>/drills/review/<focus><ext>`) and ask for one line per change: which issue it fixes. The fix and that comparison go into the report.

## explain drill: work (optional)
The learner explains, from memory, a part of their current work project they only partly understand: what it does, inputs and outputs, edge cases, why it is written that way. Do NOT ask for or accept pasted work code; work only from their explanation. Ask the follow-up questions a senior colleague or interviewer would ask, list the gaps to look up, and log `dojo.py log drill 20 work-explain`. See `progress/docs/WORK_HABITS.md` if it exists.

## explain drill
Give a task and ask them to answer WITHOUT code, using the five steps in `docs/INTERVIEW_PLAYBOOK.md` ("When you cannot write something"): concept and approach, skeleton, the precise thing to look up, how to verify, trade-offs. Score each step out of 2 and say what was missing.
