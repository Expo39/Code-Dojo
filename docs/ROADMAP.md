# Roadmap: which tracks, in what order, in what mix

The dojo is practical, but a learner rarely wants only one thing: "Python for interviews, C++
later, robotics one day", "web back ends, then data", "C for embedded work". The roadmap
decides the order and the mix of tracks from the learner's goals and their measured progress,
and changes it when either changes. These rules are shared; each learner's roadmap is personal
and lives in `progress/PLAN.md`. The `dojo-roadmap` skill runs it.

## 1. Start from the learner, and ask when something is missing

First, two choices for the learner as a whole (`profile.json`, asked by `dojo.py setup`, changed
any time):

| Mode | For | What it changes |
| --- | --- | --- |
| `interview` | live-coding interviews, with or without a date | the most Perform practice, a mock every week, the interview playbook |
| `hybrid` | interview-ready while growing as an engineer | the default balance, a mock every two weeks |
| `industry` | entering an industry or role, no interview yet | more projects in that industry's style, a mock a month once applying is near |
| `hobby` | the subject for its own sake | projects and exploration, no mocks unless asked, no timed pressure |

| Target level | Means | Typical bar |
| --- | --- | --- |
| `hobbyist` | build your own things, read docs, fix your own bugs | working programs and the basics behind them |
| `junior` | job-ready: everyday code fluently, read a team's code, tests, git | easy problems fluently, reading and debugging others' code |
| `mid` | design modules, review others' code, debug unfamiliar systems | mediums, design and testing habits, performance basics |
| `senior` | architecture, deep debugging and domain depth, guiding others | the above plus design trade-offs and the domain's depth |

The mode sets how the time is spent (`METHOD.md`, weekly balance); the target level sets how far
each goal goes, together with the rules below on enough, interviews and the domain. A learner
who is unsure gets a recommendation with a reason, then decides.

Then, for each goal:

- **What and why**: the subject, and what it is for (a job, an interview, a project, a
  course, curiosity). The reason decides the priority more than the subject does.
- **How far**: the bar that is enough for this goal, in the learner's words ("solve easy
  practical problems like the ones I was asked, fluently"; "read and fix our Django code").
- **Priority order** across goals, and any **date** (interview, exam, job start).
- **Where they are now** in it (`BASELINE.md`, `dojo.py stats`, or a short check).
- **Hours** per week and how stable they are.
- **Anything that rules an order out or in**: work needs, confidence, hardware, operating system.

If one of these is unknown, ask (one or two questions at a time). Never fill a gap with a guess
about what "people like this" want.

**Enough is the target, not mastery.** AI writes much of the code today, so for most goals the
bar is good understanding and good basics: fluency at the everyday level the goal needs, plus
reading, reviewing and debugging code the learner did not write. **The domain sets the depth.**
Where a bug costs more (low-level and embedded code, real-time control, robots that move,
security, money, medical), the bar goes deeper: memory and undefined behaviour, testing,
debugging and review rigour, the failure modes of that domain. Say which applies, and why, when
setting a bar. Train to the bar, then move the track to maintenance. Never add depth,
modules or milestones the goal does not need; a harder milestone in a track README is an option,
not a duty. If the learner asks for more later, raise the bar then.

**An interview (or exam) goal aims to do great, at that company's standard.** When the learner
names the company or the exam, ask what is known of its standard: the format, the level of the
problems, the topics and languages the role names, past questions. Set the bar from that, aiming
to pass it comfortably, not just scrape through. If nothing is known, play safe: the track's
interview-ready milestone (in Python, M2) plus every topic the role names. Record the standard
and the bar in `progress/docs/INTERVIEW_PREP.md`; when the interview is over, the bar returns to
the learner's everyday one.

**Record the goal, not the tool.** "Robotics", "data work" or "web back ends" is the goal;
ROS, pandas or a framework are tools inside it. A far-off goal stays a goal in the plan, and the
branch within it (perception, control or learning-based robotics, say) and the tracks it needs
are chosen when it comes up, from what the learner wants then. A choice made that late can still
change earlier rings (which second language, how deep), so the roadmap review before such a
goal looks at them again.

## 2. Tracks, prerequisites and states

Each track states what it needs first: `requires` in `tracks/<track>/track.json` and a
"Prerequisites" section in its README (for example, ROS 2 needs Python and C++ basics on
Linux). A track the learner wants that does not exist yet is built when the roadmap reaches it
(section 8), not in advance.

Each track in a roadmap is in one state; measurable gates, never dates, move it to the next:

| State | Share of new-material time | Meaning |
| --- | --- | --- |
| not started | none | waiting for its start condition |
| taster | 10 to 20% | first modules, alongside a main track |
| main | the rest | where most new material comes from |
| priority | 80 to 100% | a dated goal is close; everything else is in maintenance |
| maintenance | 0% (`mix <track>=0`) | redos only, so it does not fade |
| done | 0% | the learner's bar for it is met; redos continue while they come up |

`python dojo.py mix python=80 cpp=20` records the shares and `--priority "<text>"` the current
override; `today` then splits each day by them and keeps redos coming in every track.

## 3. Ordering rules

1. **One main track.** At most one other track is in active learning (a taster) at a time.
2. **One new language at a time.** A second language starts as a taster only once the first has
   met its first milestone gate (fundamentals fluent), so the two do not blur.
3. **Prerequisites first.** A track starts only when its `requires` are met, or when the
   learner chooses to accept the risk (record it).
4. **A dated goal wins.** In the run-up to an interview, exam or job start, its track becomes the
   priority and the others go to maintenance; afterwards, review the roadmap.
5. **Never drop a learned track to nothing.** Maintenance keeps its redo queue alive.
6. **The reason can justify a single focus.** If the learner says one track matters for their
   job or their confidence, keeping all new material there is a valid plan, not a lack of
   ambition. Record when the other goals will be revisited.
7. **The learner decides.** The tutor recommends an order with its reasons and its cost; if the
   learner prefers another, record the choice and the risk once, then follow it.

## 4. The cost of a choice, from the learner's own data

Never quote generic durations ("C++ takes six months"). Estimate from the log: the learner's
recent rate (modules or gate progress per week of real hours) gives the date of the next gate;
moving X% of the time to another track moves that date by roughly X%. Show the arithmetic in one
or two lines and give a range. With less than two weeks of data, say the estimate is rough.
Shared files (track READMEs, docs) never hold time estimates; they live only in `PLAN.md`.

## 5. Bridges between tracks

When a second language starts, teach from what the learner already knows: name the equivalent
in their first language ("a Python list; in C++ a `std::vector`"), and say in one line where the
two differ. Cheat-sheet bullets for the new track include the comparison.

## 6. Theory, just in time

The dojo learns by doing, so theory comes only when the next practical step needs it, and only
as much as that step needs. Each module's `primm/README.md` may have a `Theory:` line (Big-O
before hashing, the memory model before pointers, coordinate frames before tf2). Before the first
exercise of such a module the tutor asks:

> "This module relies on <theory>. Want a short theory lesson first, or do you know it already?"

A theory lesson is a `teach me` lesson in theory form (`dojo-teach`): predictions are answered on
paper, the run step is a short demo or measurement, and it ends by applying the idea in a few
lines of code. If the learner skips it, note it in `PLAN.md`; when they then struggle on exactly
that idea, offer it again (once) before a hint.

## 7. When the roadmap is reviewed

- **Every session** (`dojo-session`), a quick check for triggers; say something only if one fires:
  - a milestone gate was met (`dojo.py stats`), or a track's modules ran out;
  - a date was set, changed or entered its run-up;
  - the learner mentioned a new goal, dropped one, or changed their hours for good;
  - progress has stalled (no gate progress, or the same weak spot, for 3 weeks);
  - the real split (`dojo.py stats`) is more than 15 points off the mix for 2 weeks.
  
  On a trigger, one line: "<what happened>: this may change the plan. Review it now (5
  minutes) or at the weekly review?" Never change the plan silently.
- **Every week** (`dojo-weekly`): the mix against the real split, gate progress per track, and a
  settings review (`dojo.py settings --review`): each suggested change is one yes-or-no question
  to the learner, and only the yes answers are applied.
- **Every month** (`dojo-assess`), and whenever the learner says `replan`.

## 8. Writing it down, and building a missing track

`progress/PLAN.md` has a **Roadmap** section (a table: track, state, share, start condition,
why), a **Skill tree** drawn from the same goals (rings in priority and prerequisite order, each
naming the goal it serves; `TRACKS.md`), and a **Plan changes** log (date, change, reason), so
the learner can always see why the plan looks as it does. `profile.json` holds the same mix and priority (`dojo.py mix`).

When a track reaches taster state but is only a placeholder (a README without `track.json`):
agree its toolchain with the learner (a container keeps the host clean and is the suggested
default for compilers and frameworks), write `track.json` and the module list in its README
(`docs/TRACKS.md`), and generate only the first module (`dojo-new-exercise`).
