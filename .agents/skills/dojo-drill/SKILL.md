---
name: dojo-drill
description: Short drills for reading, debugging and recognising code in the Code Dojo. Use when the learner says "read drill", "debug drill", "discriminate drill", "work drill", "practise <concept>", or an older name ("predict" or "trace drill" = read drill; "bug" or "review drill" = debug drill).
---

# Drills

Wait for the learner's "go" before writing or showing a drill, even when the session template says a drill is next (`AGENTS.md`: everything waits for their go). A drill that needs files (a debug drill, a read snippet the learner keeps) follows the same layout in its own type folder: `workspace/<track>/drills/<type>/<focus><ext>` with that folder's tests and `.history/` only when the drill needs them (a debug drill has both; a read snippet neither) (`AGENTS.md`, generated files). Always NEW material, written for the drill: never reuse exercise files or reveal anything from `.solutions/`. Match the learner's current level (`progress/PLAN.md`) and target their recurring mistakes (`progress/BASELINE.md`, `progress/<track>/mistakes.md`, `progress/mistakes.md`). Pitch drills so the learner gets about 85% of the individual steps right: easier wastes the time, harder teaches nothing. Never ask how sure they are: read it from the wording (`AGENTS.md`, predict then run); "I don't know" is a gap, not a wrong answer. Log each drill: `dojo.py log drill <minutes> <type> --result <right|wrong> --confidence N`; log wrong answers with `dojo.py mistake` (a wrong answer at 80 or more is a misconception: say so in the mistake row).

## Report (every drill with an answer)

After scoring, write `progress/<track>/drills/<DD-MM-YYYY>_<type>_<focus>.md` (a name already taken gets `_2`): a header (the drill file, and its `.history/` original if it has one; the task in one line; the minutes), then
1. **My answer**: what the learner said, in their words, close to verbatim; for a second pass after a prompt, a separate list, saying what prompted it.
2. **The real issues** (or the right answers): a table with the line, the problem and why it is wrong, in words; never the fixed code.
3. **Comparison**: found on the first pass, found after a prompt, missed, false alarms (and any fair suggestion that is not a bug).
4. **The habit to take away**, one or two lines.
Read drills in chat get the same report (their predictions or table against the real values). The weekly review and the progress coach read these reports.

## practise <concept(s)>

Drills drawn from the concept graph (`dojo.py graph next`, or the concepts the learner names). Mix the concepts: never two questions in a row on the same one, since an answer that is still fresh in mind trains nothing. Per concept, in this order, dropping back a step when one fails: recall (a short predict or trace where the concept is not named), then discriminate (below, against the concept it is most often confused with), then compose (a debug drill that needs it with one or two others). A retry after a wrong answer comes later in the set, on a different surface.

## read drill
"What does this code produce?", in chat. Pick the form the code calls for, and mix the two across a set:
- **Predict**: a 5 to 12 line snippet (a language gotcha or a small algorithm); they say what it prints. Draw first from the learner's own traps in `progress/docs/PITFALLS.md` and recent rows of the mistakes logs. Ask for the prediction and wait; give the run command only in the next message, never in the same one. After their answer, reveal and explain, and name the concept. Three in a row unless asked otherwise.
- **Trace**: a 10 to 20 line function with a loop and one input; they write the value of each variable after each iteration (a trace table, on paper or as comments). Check the table row by row.
A snippet the learner keeps goes in `workspace/<track>/drills/read/<focus><ext>`.

## debug drill
Code with one to three realistic bugs and failing tests; the learner finds, confirms and fixes every one. Often present it as "an AI assistant wrote this; would you merge it?" (catching plausible-but-wrong code is the most important AI-age reading skill). Pitch it by size: a 5 to 15 line function with ONE bug, or 15 to 40 lines with two or three, never more bugs than the tests show. The bugs are correctness and edge cases a test can catch; style, naming or slowness the learner points out are discussed after the tests pass, never planted as the task.

Write the code to `workspace/<track>/drills/debug/<focus><ext>`, where `<focus>` is the function's name in snake_case (`find_owner`; never a name that gives a bug away; a name already taken gets `_<DD_MM_YYYY>`), and its test file in the same type folder at the track's `test_file` pattern (`drills/debug/tests/test_<focus>.py` in Python; only the drill files sit in `drills/debug/`; create the folders if needed; these are your files, so writing them is allowed). The repo runs pytest with `--import-mode=importlib`, so a Python drill test adds the folder above it (`Path(__file__).parent.parent`) to `sys.path` before importing the drill. Copy the untouched file to `workspace/<track>/drills/debug/.history/<focus>_original<ext>` (never edited, so after the fix the learner compares the two with `diff`); check the tests fail before handing it over. The docstring shows the main example AND a `Check your fix with:` input printed without its output, which varies a different parameter or shape from the example (another `k`, another length) so that a fix that only repairs the example fails on it; the learner traces it before and after the fix. The test file covers both.

Order: the learner reads it first and lists what they think is wrong (the first-pass list the report scores), then predicts which tests fail, and only then gets the run command (the track's test command on that file, e.g. `.venv/bin/python -m pytest -q workspace/python/drills/debug/tests/test_<focus>.py`; in the editor, "Debug: this file" runs it with breakpoints). Each bug: a hypothesis, confirmed in the debugger, fixed with the smallest change. After the tests pass, give the comparison command (`! diff workspace/<track>/drills/debug/.history/<focus>_original<ext> workspace/<track>/drills/debug/<focus><ext>`) and ask them to say in one line per bug what the fix changed and why. Never reveal a bug before they find it; hints follow the ladder.

## work drill (optional)
Triggered by "work drill" or "explain my work". The learner explains, from memory, a part of their current work project they only partly understand: what it does, inputs and outputs, edge cases, why it is written that way. Do NOT ask for or accept pasted work code; work only from their explanation. Ask the follow-up questions a senior colleague or interviewer would ask, list the gaps to look up, and log `dojo.py log drill 20 work`. See `progress/docs/WORK_HABITS.md` if it exists.

## discriminate drill (in chat)
Two or three short problem statements that look alike but need different patterns (a running total against a sliding window; counting against grouping; two pointers on sorted input against a hash map on unsorted). For each, the learner names the pattern and the one feature of the statement that decides it, with their confidence. No code. Score: pattern right, deciding feature right. Draw the pairs from the learner's weak spots and recent mistakes; log as `drill <minutes> discriminate`.

## Not a drill: explaining without code
There is no standalone explain drill: talking through a solution with no code for 20 minutes is not how interviews run. Perform is a timed `interview problem` (or a mock) coded while talking. The fallback for a part they cannot write (`docs/INTERVIEW_PLAYBOOK.md`, "When you cannot write something") is a move inside that problem, used when they are stuck on syntax, never a separate exercise.
