# Personal docs

The docs in `docs/` are the method, the same for everyone. Each learner also has their own docs
in `progress/docs/` (gitignored, never pushed): the method applied to them, written by the tutor
from their own data. This file is the spec, so every learner's docs have the same shape whoever
writes them and whatever the learner's goals. `dojo.py` creates the folder and its `README.md`
index; the tutor creates each file below only when it has something to say, and never fills one
with guesses: what it does not know, it asks.

Write every personal doc at the learner's level (`AGENTS.md`, Style): plain words with terms
defined for a beginner, concise for an advanced learner.

Shared docs never hold anything about one learner (names, dates, hours, their mistakes, their
job, their estimates). When something written for one learner turns up in `docs/`, move it here.

## PITFALLS.md: your own traps

- **From**: `progress/mistakes.md`. A theme that comes back 2 or more times becomes an entry.
  There is no shared list of pitfalls: what trips one learner does not trip another, so each
  learner's list is built only from their own mistakes.
- **Written by**: `dojo-weekly` (step 3, repeated mistakes); seeded by `dojo-assess` from the
  recurring mistakes in `BASELINE.md`.
- **Used by**: predict and trace drills (`dojo-drill`) draw from it first; warm-up self-checks.
- **Shape**: one table, in the learner's track language:

```markdown
| Trap | Rule | Check | Last seen |
| --- | --- | --- | --- |
| <what you did, in words> | <the correct habit> | <a self-check question that stands alone> | <date> |
```

  An entry not seen for 6 weeks moves to a "Retired" section at the bottom.

## WEEK.md: your weekly rhythm

- **From**: `profile.json` (minutes per day, rest days) and the roadmap's mix.
- **Written by**: `dojo-assess` at placement; `dojo-roadmap` or `dojo-weekly` when the hours or
  the mix change.
- **Shape**: one table, a row per day: the session template from `docs/DAILY_SESSION.md` that
  fits that day's minutes, and the day's extra from its "weekly rhythm" (mid-week drill day,
  mock day at the frequency the mode sets, weekly review, rest). With several tracks, which
  blocks go to which track.

## INTERVIEW_PREP.md: only when an interview is a goal

- **From**: the learner's goal and date (`profile.json` `target_date`, `PLAN.md`).
- **Written by**: `dojo-roadmap` when an interview becomes a goal or gets a date; `dojo-mock`
  adds what each mock showed.
- **Shape**: the company and role, what its standard is known to be (format, level, topics; ask)
  and the bar set from it (`docs/ROADMAP.md`: do great at that standard; unknown means the safe
  side); the run-up plan from
  `docs/INTERVIEW_PLAYBOOK.md` with real dates once a date exists; 3 stories about their work
  (problem, what they did, result, what they learned), written by the learner in their words;
  questions to ask the interviewer; the two habits the latest mock asked for.

## WORK_HABITS.md: only for a learner who already works in the field

- **From**: a short conversation about their job and how they use AI there (ask; never assume
  a job).
- **Written by**: `dojo-assess`, or on request.
- **Used by**: `explain drill: work` (`dojo-drill`) and one no-pressure question in `dojo-weekly`.
- **Shape**: the principle (work and the dojo stay separate), at most three habits that make AI
  use at work build understanding, and how to tell they are working.

## Other personal files (not in `progress/docs/`)

`PLAN.md` (goals, roadmap, milestones, estimates), `BASELINE.md`, `cheatsheet.md`,
`mistakes.md`, `approaches.md`, `revisits.md`, `weekly/` and `mocks/` stay at the top of
`progress/`: the tracker and the skills read them there.
