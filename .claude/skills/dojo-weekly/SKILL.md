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
   - Repeated mistakes (the same theme 2 or more times): name the habit to build.
   - Mock result and the two habits from it.
   - Balance across strands (learn, write, read and debug, build, perform; `docs/METHOD.md`).
4. Write the "Coach notes" section of `progress/weekly/<week>.md`: 3 wins backed by numbers, 3 things to fix, and next week's focus: modules, which weak spots get a `teach me` first, project milestone, mock day.
5. Update `progress/PLAN.md` "Current focus". If a milestone gate is met (`stats`), congratulate them with the evidence and update the milestone table. If progress is far off the estimates for 3 or more weeks, re-estimate honestly and explain why.
6. Run `dojo.py export` if the profile has an `export_target` (weekly backup).
7. Tell the learner the summary in 6 to 8 lines. End with one specific thing they did better than a month ago.
