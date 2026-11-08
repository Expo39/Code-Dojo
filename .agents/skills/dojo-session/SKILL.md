---
name: dojo-session
description: Start-of-session catch-up for the Code Dojo learner. Use on the learner's first message of every session, or when they say "catch up", "where am I", "what's today". Syncs untracked work, reads their plan and reports, and proposes today's session.
---

# Session catch-up

Keep the whole catch-up to a few minutes. Use `python3 dojo.py` on Linux/macOS, `python dojo.py` on Windows.

1. If `progress/profile.json` is missing: the learner is new. Welcome them in two lines and offer to set them up here and now (the `dojo-assess` skill, step 0), or, if they prefer a terminal, `python dojo.py setup`. Stop the catch-up here.
2. Run `dojo.py sync`. For exercises edited but not logged, ask once, as one short list, roughly how long each took and how much help they had; log each with `dojo.py done <item> --minutes N --hints H` (skip what they do not remember). For timers left running, ask, then `done --minutes N` or `cancel`.
3. **Changes to the tracks.** Short, and never during an exercise.
   - Updates on the shared repo: run `dojo.py update` (it lists incoming commits and the files that
     run code), tell the learner in two lines, and only after their yes `dojo.py update --yes`.
   - Track changes (only modules they have started or finished are listed): one line per module,
     at most five, then one question, e.g. "m01 gained floats and rounding (split_bill), m02
     `match` (route_command). Add them to your queue, go one by one, or decide later?"
   - Apply: learn it, nothing to do (a lesson topic: `teach me` now, or a note under Current focus);
     already know it, `dojo.py mark <slugs> --box 3`; not for me, `dojo.py settings
     skip_exercises+=<slugs>` (or `skip_modules+=<module>`). A changed exercise: one line on what
     changed, then redo it, already know it, or leave it out. Removals: one line each.
   - "Later": ask again next session, never twice in one. Otherwise `dojo.py changes --ack`; log
     exclusions under Plan changes. A new module or track touching a goal is a roadmap trigger.
4. Run `dojo.py today`. Read `progress/PLAN.md` ("Current focus"), the newest `progress/weekly/*.md` coach notes, and the last rows of `progress/mistakes.md`.
5. Ask: "Anything you practised without me, or anything that felt shaky?" Log mistakes with `dojo.py mistake` and add cheat-sheet bullets for the concepts involved.
6. Check the roadmap triggers (`docs/ROADMAP.md`, section 7) against `today`, `stats` when a gate may have moved, and what they just told you. If one fires, say it in one line and offer `dojo-roadmap` now (5 minutes) or at the weekly review; otherwise say nothing about it.
7. Tell them, in 4 to 6 lines: time today and this week against the plan, what is due in the redo queue, the next new material (per track, following the mix, when there are several), any weak spot, and the session template for today's time (`docs/DAILY_SESSION.md`, `progress/docs/WEEK.md`), reordered so the strands `today` reports as short come first after the redo queue. If the module about to start has a `Theory:` line, offer the theory lesson first. If behind, suggest the capped catch-up from `today`; never guilt.
8. Remind them in one line of this week's habit focus from the coach notes (for example "say your plan before typing"), if there is one.
9. Run `dojo.py session start` (the session clock: warm-up, explanations and feedback between exercise timers count as study when it ends), then name the first block (usually the warm-up, then the redo queue) and wait for their "go" before starting it, as for every later block. Pause it (`session pause` / `resume`) for breaks, time away and dojo maintenance; run `session end` at the end of day, before `today`.

If today is the last training day of the week, remind them of the weekly review and, if their mode has a mock this week (`docs/METHOD.md`), of the mock interview (`dojo-mock`, `dojo-weekly`). On a rest day, say so; if they still want to train, a short session counts.
