---
name: dojo-session
description: Start-of-session catch-up for the Code Dojo learner. Use on the learner's first message of every session, or when they say "catch up", "where am I", "what's today". Syncs untracked work, reads their plan and reports, and proposes today's session.
---

# Session catch-up

Keep the whole catch-up to a few minutes. Use `python3 dojo.py` on Linux/macOS, `python dojo.py` on Windows.

1. If `progress/profile.json` is missing: the learner is new. Point them to `python dojo.py install`, `python dojo.py setup`, then run the `dojo-assess` skill. Stop here.
2. Run `dojo.py sync`. For exercises edited but not logged, ask once, as one short list, roughly how long each took and how much help they had; log each with `dojo.py done <item> --minutes N --hints H` (skip what they do not remember). For timers left running, ask, then `done --minutes N` or `cancel`.
3. Run `dojo.py today`. Read `progress/PLAN.md` ("Current focus"), the newest `progress/weekly/*.md` coach notes, and the last rows of `progress/mistakes.md`.
4. Ask: "Anything you practised without me, or anything that felt shaky?" Log mistakes with `dojo.py mistake` and add cheat-sheet bullets for the concepts involved.
5. Tell them, in 4 to 6 lines: time today and this week against the plan, what is due in the redo queue, the next new material, any weak spot, and the session template for today's time (`docs/DAILY_SESSION.md`). If behind, suggest the capped catch-up from `today`; never guilt.
6. Remind them in one line of this week's habit focus from the coach notes (for example "say your plan before typing"), if there is one.
7. Start the first block (usually the warm-up, then the redo queue) unless they want something else.

If today is the last training day of the week, remind them of the mock interview and the weekly review (`dojo-mock`, `dojo-weekly`). On a rest day, say so; if they still want to train, a short session counts.
