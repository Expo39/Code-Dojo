---
name: dojo-roadmap
description: Plan which tracks a Code Dojo learner follows, in what order and mix, from their goals and measured progress. Use when the learner says "plan my learning", "replan", "I want to learn X", "when should I start X", "should I learn X before Y", "I have an interview/exam on <date>", "focus on X", during placement (dojo-assess), or when a roadmap trigger fires in a session or weekly review.
---

# Roadmap

The rules are in `docs/ROADMAP.md`; read it first. Everything written here is personal and stays
in `progress/` (gitignored). Use `python3 dojo.py` on Linux/macOS, `python dojo.py` on Windows.

1. **Read**: `progress/profile.json`, `progress/PLAN.md` (Roadmap, Plan changes, milestones),
   `progress/BASELINE.md`, `dojo.py mix`, `dojo.py stats`, and each relevant track's
   `track.json` (`requires`) and README (Prerequisites, Theory). List the tracks that exist and
   the ones that are placeholders.
2. **Fill the gaps by asking** (ROADMAP section 1): for each goal the what and why, how far is
   enough (the bar, in their words), the priority order, any date, the current level, the hours, constraints. One or two questions at a time;
   skip what the files already answer. Never assume a goal or its order.
3. **Recommend**: for each track, its state, share, start condition (a gate, not a date) and the
   bar that ends it (then maintenance); schedule only the modules that bar needs (for an
   interview or exam goal, the bar comes from the company's or exam's standard, or the safe side
   when it is unknown: ROADMAP section 1),
   following the ordering rules (section 3). Give the reason for each in one line and the cost
   from the learner's own data (section 4). If the learner asked about one track ("when do I
   start ROS?"), answer that directly: what it needs first, how far they are from it, and what
   starting earlier would cost.
4. **Let them decide.** If they choose differently, say the risk once, then follow their choice.
5. **Write it down**:
   - `progress/PLAN.md`: the Roadmap table (track, state, share, start condition, why) and a dated
     line under Plan changes with the reason; update Current focus if it changes now. Redraw the Skill
     tree from the goals so its rings match the table (`docs/TRACKS.md`), and keep milestone
     estimates consistent with both.
   - `progress/docs/` (spec: `docs/PERSONAL_DOCS.md`): update `WEEK.md` when the mix or the hours
     change; create or update `INTERVIEW_PREP.md` when an interview is a goal or gets a date.
   - `dojo.py mix <track>=N ...` (shares sum to 100, 0 = maintenance) and `--priority "<text>"`
     for a dated or stated override (`--priority ""` clears it). Add the track to the profile if
     needed (`mix` does it).
6. **If a track starts now and is a placeholder**: agree the toolchain, write its `track.json`
   and README modules (`docs/TRACKS.md`), then generate the first module only (`dojo-new-exercise`).
   Shared track files go in git; the learner's choice does not.
7. **Close** in 3 to 5 lines: the order, this week's mix, what moves each track to its next state,
   and when the roadmap will next be looked at.
