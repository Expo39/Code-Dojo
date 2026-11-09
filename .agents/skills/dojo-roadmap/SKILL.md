---
name: dojo-roadmap
description: Plan which tracks a Code Dojo learner follows, in what order and mix, from their goals and measured progress. Use when the learner says "plan my learning", "replan", "I want to learn X", "when should I start X", "should I learn X before Y", "I have an interview/exam on <date>", "focus on X", during placement (dojo-assess), or when a roadmap trigger fires in a session or weekly review.
---

# Roadmap

Rules: `docs/ROADMAP.md` (read it first). Everything written here is personal (`progress/`).

1. **Read**: `profile.json`, `PLAN.md` (Roadmap, Plan changes, milestones), `BASELINE.md`,
   `dojo.py mix`, `dojo.py stats`, `dojo.py graph next`, and each relevant track's `track.json`
   (`requires`), README (Prerequisites, Theory) and `graph.json`. Note which tracks exist and which
   are placeholders.
2. **Ask what is missing** (ROADMAP section 1), skipping what the files answer: mode and target
   level if unset or no longer true; per goal the what and why, the bar, priority, date, current
   level, hours, constraints. Never assume a goal or its order. For a new goal or a track they
   have not started, when the track has a concept graph, run the probe (`dojo-probe`) before
   recommending: `dojo.py graph path <goal>` then gives what is really left, which the estimate
   is built from. That path crosses tracks: a concept needing `<track>:<id>` names a track that
   must come first or run alongside (robotics needs C++ pointers); say so and plan that track's
   concepts, not its whole syllabus, into the roadmap.
3. **Recommend** per track: state, share, start condition (a gate) and the bar that ends it, with
   only the modules that bar needs (an interview or exam bar comes from its standard, or the safe
   side). Follow the ordering rules (section 3); one line of reason each, and the cost from their
   own data (section 4). Asked about one track ("when do I start ROS?"): what it needs first, how
   far they are, what starting earlier costs.
4. **They decide.** A different choice: state the risk once, then follow it.
5. **Write it down**:
   - `PLAN.md`: Roadmap table (track, state, share, start condition, why), a dated Plan changes
     line, Current focus if it changes; redraw the skill tree to match (`docs/TRACKS.md`) and keep
     estimates consistent.
   - `progress/docs/`: `WEEK.md` when mix or hours change; `INTERVIEW_PREP.md` when an interview
     becomes a goal or gets a date.
   - `dojo.py mix <track>=N ...` (sum 100, 0 = maintenance) and `--priority "<text>"` (`""`
     clears it).
6. Modules move in or out: show `dojo.py modules` and agree them (`dojo-assess`, 3b).
7. A track starting now that is a placeholder: design it with `dojo-new-track` (research,
   toolchain agreed with the learner, first module only).
8. **Close** in 3 to 5 lines: the order, this week's mix, what moves each track on, and when the
   roadmap is next reviewed.
