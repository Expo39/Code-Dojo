---
name: dojo-weekly
description: Weekly review for the Code Dojo learner. Use when the learner says "weekly review", "how was my week", at the end of their last training day, or when a weekly report is missing for a finished week.
---

# Weekly review (about 20 minutes)

1. Run `dojo.py week --write` (add `--date YYYY-MM-DD` for a past week) and `dojo.py stats`.
2. Read: the report, `progress/PLAN.md`, last week's coach notes, this week's `progress/mocks/`, and the week's rows in `progress/mistakes.md`.
3. Analyse honestly, with numbers:
   - Time against the plan, and why (ask; do not assume). If short, adjust the plan or the profile's hours rather than piling up debt; a capped catch-up of at most an hour a day is fine.
   - Speed and hints per pattern: anything with a median above 1.5x or more than 1.5 hints is a weak spot.
   - Repeated mistakes (the same theme 2 or more times): name the habit to build, and add or
     update its row in `progress/docs/PITFALLS.md` (last seen date; retire rows unseen for 6
     weeks; spec in `docs/PERSONAL_DOCS.md`).
   - Mock result and the two habits from it.
   - Follow-up methods in `progress/approaches.md` not yet tried: list them (one line each) as optional bonus work.
   - Process: the report's "Process" line (how often every step was followed, the most skipped step). A step skipped 3 or more times becomes next week's habit focus, with a one-line reminder the tutor gives at every exercise.
   - Balance across strands (learn, write, read and debug, build, perform) against the shares for
     their mode (`docs/METHOD.md`); a missed mock counts only if the mode had one due.
   - Roadmap: with several tracks, the real split (`stats`, "Track time") against the mix; gate
     progress per track; any trigger from `docs/ROADMAP.md` section 7. If one fired, run
     `dojo-roadmap` with the learner (or carry the question to next week if they prefer).
4. Write the "Coach notes" section of `progress/weekly/<week>.md`: 3 wins backed by numbers, 3 things to fix, and next week's focus: modules, which weak spots get a `teach me` first, project milestone, mock day.
5. Update `progress/PLAN.md` "Current focus". If a milestone gate is met (`stats`), congratulate them with the evidence and update the milestone table. If progress is far off the estimates for 3 or more weeks, re-estimate honestly and explain why.
6. **Settings review, yes or no.** Run `dojo.py settings --review`. For each suggestion, and for
   the judgement calls it lists (mode, target level, priority, tracks, skipped modules) where this
   week's evidence or what the learner said points to a change, ask one short yes-or-no question
   with the evidence ("Wednesdays averaged 20 minutes against 90 planned: set Wednesday to 15?").
   Apply only the yes answers (`dojo.py settings key=value ...`, `dojo.py mix ...`) and add a line
   under Plan changes in `progress/PLAN.md` for each. A no is fine and changes nothing; do not ask
   the same question again next week unless the evidence has grown.
7. Run `dojo.py export` if the profile has an `export_target` (weekly backup).
8. Ask one short question about work: which of the three habits in `progress/docs/WORK_HABITS.md` (if the file exists) they used this week. No numbers, no pressure.
9. Tell the learner the summary in 6 to 8 lines. End with one specific thing they did better than a month ago.
