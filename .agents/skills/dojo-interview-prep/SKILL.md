---
name: dojo-interview-prep
description: Set up, run and close the checklist for one interview in the Code Dojo. Use when the learner says an interview is close, "I have an interview on <date>", "prepare me for <company or role>", asks for a custom track for an interview, or when `today` says an interview has passed and must be closed out.
---

# Interview preparation checklist

Rules: `docs/CHECKLISTS.md`, section 8 (read it first). The point is a single written list of what
the learner wants to prepare, so the preparation stays on it. Everything written here is personal
(`progress/`). Use `python3 dojo.py` on Linux/macOS, `python dojo.py` on Windows.

## Set up

1. **Ask**, a few at a time and skipping what the files already answer: the date, the role or
   company, the format (discussion, live coding, take-home, system design), what the learner
   already knows they want to cover, and the time they have until then (`dojo.py settings`).
2. **Propose gaps, never impose**: from `progress/docs/INTERVIEW_PREP.md`, the relevant track's
   concept graph (`dojo.py graph path <goal>`), `docs/INTERVIEW_PLAYBOOK.md` and the stats, name
   what an interview of that format usually asks that the learner did not list. The learner
   accepts or strikes each one; striking is final.
3. **Write the list**: `dojo.py interview start <name> <DD/MM/YYYY>`, then fill the file it
   names (`progress/interviews/<DD-MM-YYYY>_<name>.md`). One line per item,
   `- [ ] topic | how it is practised (read, drill, mock) | done when <observable bar>`, ordered by
   how likely it is to come up and how weak the learner is on it. Anything they decline goes under
   Out of scope.
4. **A custom track**, when the material does not exist (a company's stack, a tool): hand over to
   `dojo-new-track` with these items as its scope, personal (`tracks_personal/`) unless the learner
   says otherwise. The track covers the items and nothing else.
5. **Sprint**: `dojo.py interview start` has set `sprint_until` to the date; offer the sprint's
   redos (`dojo.py settings sprint_redos=<N>`, `dojo-roadmap`), put a dated line under Plan changes
   in `PLAN.md` with the link to the checklist, and `dojo.py mix --priority "<interview, date>"`.

## While it is open

- Each block takes the next unchecked item and its "how". Say the item and its time box when it
  starts and when it ends.
- Tick it with `dojo.py interview check <n>` only when its done-when bar was met in front of you.
- Gap: one short explanation that still follows the learner's overrides (what the thing is, the
  problem it solves, one concrete example), a few lines, then back to the questions. No lesson, no
  new note files, no reading list; a bigger gap becomes a parked item or a new checklist item the
  learner chooses to add.
- Tangent, however useful: `dojo.py interview park "<one line>"`, say "parked", and carry on. No
  web lookups outside the item's own source.
- Never add an item, drop one or reorder the list without the learner's say.

## Close

After the date, or when the learner says it is over: `dojo.py interview close` (archives the
checklist, clears the sprint and the priority). Then, in this order: how it went (two lines, for
`INTERVIEW_PREP.md`); offer the parking lot as the first new material; ask whether to keep training
for interviews (`dojo.py mode`, `docs/METHOD.md`); replan with `dojo-roadmap`, which restores the mix
and writes the Plan changes line.
