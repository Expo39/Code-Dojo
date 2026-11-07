---
name: dojo-session
description: Start-of-session catch-up for the Code Dojo learner. Use on the learner's first message of every session, or when they say "catch up", "where am I", "what's today". Syncs untracked work, reads their plan and reports, and proposes today's session.
---

# Session catch-up

Keep the whole catch-up to a few minutes. Use `python3 dojo.py` on Linux/macOS, `python dojo.py` on Windows.

1. If `progress/profile.json` is missing: the learner is new. Welcome them in two lines and offer to set them up here and now (the `dojo-assess` skill, step 0), or, if they prefer a terminal, `python dojo.py setup`. Stop the catch-up here.
2. Run `dojo.py sync`. For exercises edited but not logged, ask once, as one short list, roughly how long each took and how much help they had; log each with `dojo.py done <item> --minutes N --hints H` (skip what they do not remember). For timers left running, ask, then `done --minutes N` or `cancel`.
3. **Changes to the tracks.** If the status shows updates on the shared repo, offer to pull them (`dojo.py update`, after a yes). If it shows track changes (`dojo.py changes` for details), ask about them grouped by module, one short question per group: "3 new exercises in m03 (a, b, c): learn them, already know them, or not for you?" Apply the answer: learn it, nothing to do; already know it, `dojo.py mark <slugs> --box 3` (they come back later as a check); not for me, `dojo.py settings skip_exercises+=<slugs>` (or `skip_modules+=<module>` for a whole module). For a changed exercise already in their redo queue, say in one line what changed (task, tests or clarify answers) and keep it. Removed exercises need no question. Then `dojo.py changes --ack`, and log any exclusion under Plan changes. A new module or track that touches their roadmap is a roadmap trigger (step 6).
4. Run `dojo.py today`. Read `progress/PLAN.md` ("Current focus"), the newest `progress/weekly/*.md` coach notes, and the last rows of `progress/mistakes.md`.
5. Ask: "Anything you practised without me, or anything that felt shaky?" Log mistakes with `dojo.py mistake` and add cheat-sheet bullets for the concepts involved.
6. Check the roadmap triggers (`docs/ROADMAP.md`, section 7) against `today`, `stats` when a gate may have moved, and what they just told you. If one fires, say it in one line and offer `dojo-roadmap` now (5 minutes) or at the weekly review; otherwise say nothing about it.
7. Tell them, in 4 to 6 lines: time today and this week against the plan, what is due in the redo queue, the next new material (per track, following the mix, when there are several), any weak spot, and the session template for today's time (`docs/DAILY_SESSION.md`, `progress/docs/WEEK.md`). If the module about to start has a `Theory:` line, offer the theory lesson first. If behind, suggest the capped catch-up from `today`; never guilt.
8. Remind them in one line of this week's habit focus from the coach notes (for example "say your plan before typing"), if there is one.
9. Start the first block (usually the warm-up, then the redo queue) unless they want something else.

If today is the last training day of the week, remind them of the weekly review and, if their mode has a mock this week (`docs/METHOD.md`), of the mock interview (`dojo-mock`, `dojo-weekly`). On a rest day, say so; if they still want to train, a short session counts.
