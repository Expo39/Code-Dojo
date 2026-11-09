---
name: dojo-weekly
description: Weekly review for the Code Dojo learner. Use when the learner says "weekly review", "how was my week", at the end of their last training day, or when a weekly report is missing for a finished week.
---

# Weekly review (about 20 minutes)

1. Run `dojo.py week --write` (add `--date DD/MM/YYYY` for a past week) and `dojo.py stats`.
2. Read: the report, `progress/PLAN.md`, last week's coach notes, this week's `progress/<track>/mocks/`, `progress/<track>/drills/` (what was missed and the false alarms) and `progress/<track>/probes/` for each track, the week's rows in `progress/mistakes.md` and each `progress/<track>/mistakes.md`, and `dojo.py graph next`.
3. Analyse honestly, with numbers:
   - Time against the plan, and why (ask; do not assume). If short, adjust the plan or the profile's hours rather than piling up debt; a capped catch-up of at most an hour a day is fine.
   - Speed and hints per pattern: anything with a median above 1.5x or more than 1.5 hints is a weak spot.
   - Understanding: misconceptions and fragile concepts still open in the graph, and the
     calibration lines in `stats` (stated confidence against results). Confidently wrong answers
     go into next week's repairs; consistent under-confidence is worth one line of
     encouragement backed by the numbers.
   - Repeated mistakes (the same theme 2 or more times): name the habit to build, and add or
     update its row in `progress/docs/PITFALLS.md` (last seen date; retire rows unseen for 6
     weeks; spec in `docs/PERSONAL_DOCS.md`).
   - Mock result and the two habits from it, if the mode had one this week.
   - Notes in the right place: a row or bullet in a track's `mistakes.md` or `cheatsheet.md` that
     holds in any language (reading the task, complexity, a pattern, interview technique) moves to
     the shared file at the top of `progress/`, and a language rule in a shared file moves to its
     track's (`docs/PERSONAL_DOCS.md`).
   - Follow-up methods in `progress/<track>/approaches.md` and `progress/approaches.md` not yet tried: list them (one line each) as optional bonus work.
   - Process: the report's "Process" line (how often every step was followed, the most skipped step). A step skipped 3 or more times becomes next week's habit focus, with a one-line reminder the tutor gives at every exercise.
   - Balance across strands (learn, write, read and debug, build, perform) against the shares for
     their mode (`docs/METHOD.md`); a missed mock counts only if the mode had one due.
   - Roadmap: with several tracks, the real split (`stats`, "Track time") against the mix; gate
     progress per track; any trigger from `docs/ROADMAP.md` section 7. If one fired, run
     `dojo-roadmap` with the learner (or carry the question to next week if they prefer).
4. Write the "Coach notes" section of `progress/weekly/<week>.md`: 3 wins backed by numbers, 3 things to fix, and next week's focus: modules, which weak spots and open misconceptions get a `teach me` or a repair first (the graph's lessons and repairs), project milestone, mock day.
5. Update `progress/PLAN.md` "Current focus". If a milestone on the way to their bar is met (`stats`), congratulate them with the evidence and update the milestone table; if a track's bar is met, propose moving it to maintenance (yes or no, step 6). If progress is far off the estimates for 3 or more weeks, re-estimate honestly and explain why.
6. **Settings review, yes or no.** Run `dojo.py settings --review`. For each suggestion, and for
   the judgement calls it lists (mode, target level, priority, tracks, skipped modules) where this
   week's evidence or what the learner said points to a change, ask one short yes-or-no question
   with the evidence ("Wednesdays averaged 20 minutes against 90 planned: set Wednesday to 15?").
   Apply only the yes answers (`dojo.py settings key=value ...`, `dojo.py mix ...`) and add a line
   under Plan changes in `progress/PLAN.md` for each. A no is fine and changes nothing; do not ask
   the same question again next week unless the evidence has grown.
7. Run `dojo.py export` if the profile has an `export_target` (weekly backup).
8. Ask one short question about work: which of the three habits in `progress/docs/WORK_HABITS.md` (if the file exists) they used this week. No numbers, no pressure.
9. Tell the learner the summary in 6 to 8 lines, at their level (`AGENTS.md`, Style). End with one specific thing they did better than a month ago.
