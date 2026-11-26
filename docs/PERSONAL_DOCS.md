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

- **From**: the mistakes logs (`progress/extra/mistakes.md` and `progress/<track>/mistakes.md`). A
  theme that comes back 2 or more times becomes an entry. There is no shared list of pitfalls: what trips one learner does not trip another, so each
  learner's list is built only from their own mistakes.
- **Written by**: `dojo-weekly` (step 3, repeated mistakes); seeded by `dojo-assess` from the
  recurring mistakes in `BASELINE.md`.
- **Used by**: read drills (`dojo-drill`) draw from it first; warm-up self-checks.
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
  side); the run-up plan from `docs/INTERVIEW_PLAYBOOK.md` with real dates once a date exists; 3 stories about their work
  (problem, what they did, result, what they learned), written by the learner in their words;
  questions to ask the interviewer; the two habits the latest mock asked for.

## WORK_HABITS.md: only for a learner who already works in the field

- **From**: a short conversation about their job and how they use AI there (ask; never assume
  a job).
- **Written by**: `dojo-assess`, or on request.
- **Used by**: `work drill` (`dojo-drill`) and one no-pressure question in `dojo-weekly`.
- **Shape**: the principle (work and the dojo stay separate), at most three habits that make AI
  use at work build understanding, and how to tell they are working.

## The rest of `progress/`

Your own tracks, if you make any, sit outside it in `tracks_personal/` (`docs/TRACKS.md`,
"Personal tracks"); `export` backs up both. What is about you and every track sits at the top; what belongs to one track sits in its own
folder, so the layout stays the same however many tracks you learn. The tracker and the skills
read the files where they are listed here; `dojo.py` creates the folders, and moves an older
flat layout into this one by itself.

```text
progress/
├── profile.json PLAN.md BASELINE.md   you, your goals and plan, across every track
├── overrides.md                       your personal rules (below)
├── log.csv reviews.json               every attempt and the redo schedule, every track
├── graph.json                         your evidence on each concept; a shared concept once
├── weekly/                            one report per week
├── docs/                              your docs (this spec)
├── extra/                             extra lessons: topics no track covers, and what holds in
│   ├── notes/                         any language. The same shape as a track's folder: study
│   ├── cheatsheet.md mistakes.md      notes (README index grouped by theme), cheat sheet and
│   └── approaches.md                  mistakes (reading the task, complexity, patterns, debugging)
├── <track>/                           one folder per track you learn (practice or theory)
│   ├── mistakes.md cheatsheet.md      what is specific to that language or tool
│   ├── approaches.md revisits.md      alternate methods; exercises to redo with a later concept
│   ├── notes/                         study notes: every explanation from the sessions, written
│   │                                  up in full, one file per topic, for revision
│   ├── drills/                        one report per drill: your answer against the real issues
│   ├── mocks/                         one report per mock interview; hidden/ holds the
│   │                                  scored hidden tests of each mock (`dojo-mock`)
│   └── probes/                        one report per probe: your goal, where your understanding
│                                      ends, every question with your answer and confidence
└── tracker/                           the tracker's bookkeeping (timers, session clock, what you
                                       have been asked about, update checks): nothing to read
```

### overrides.md: your own rules

- **From**: the learner asking for a rule to work differently for them only.
- **Written by**: the tutor, on the learner's request, one line per rule; `dojo.py overrides`
  creates the file and lists the rules.
- **Used by**: every tool: the session status (`dojo.py brief`) prints each override, and it
  wins over the shared rule it names.
- **Shape**: newest first, `- DD/MM/YYYY | <file> > <section> | <the rule as it applies to you>`,
  where `<file> > <section>` is the shared rule replaced (`AGENTS.md > Predict, then run`). A
  preference with no shared rule behind it names where it applies (`AGENTS.md > Coaching
  protocol`). A change that would suit every learner goes in the shared file instead.

### notes/: study notes

- **From**: every explanation the tutor gives in a session (a gap in a drill, a concept asked
  about, a correction, a repair after a wrong prediction).
- **Written by**: the tutor, during the session, in the same words and examples used in chat,
  as soon as the explanation lands; one file per topic, `<topic>.md` in snake_case (what it is,
  the problem it solves, a small concrete example, a table where it helps, a "Check:" question,
  "Read later"); a later explanation of the same topic extends its file.
- **Used by**: the learner, for revision (before an interview, after time away); the cheat
  sheet keeps one line per concept and points here for the detail.
- **Shape**: `notes/README.md` lists every topic (topic, date learnt, file); each file is dated
  with where it came from. Never solution code for an exercise. Shared ideas (any language) and topics
  no track covers go in `progress/extra/notes/`, grouped by theme in its README; when a track that
  fits one exists, the note moves into that track's `notes/`.

### Where notes go

A note goes where it is true: "`range` stops before its end" in `python/cheatsheet.md`, "name
Big-O with the input's own variable" in the shared one. The weekly review moves a note that turns
out to hold in every language up to the shared file.
