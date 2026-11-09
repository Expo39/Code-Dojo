# Code Dojo

A personal training system for becoming a strong engineer: learn to **write** code from a
blank file, **understand** code you did not write, and **perform** in live-coding interviews.
An AI coding agent (Claude Code, Codex or Gemini CLI) acts as a tutor that explains,
questions, hints and reviews, but never writes your code for you.

It works for anyone, at any level, for any subject. You tell it:

- **why you train**: interview prep, interview plus growth, entering an industry, or a hobby;
- **what level of programmer you want to become**: hobbyist, junior, mid or senior;
- **what you want to learn, and how far is enough**: good basics and understanding, or more
  where a job, an interview or the field needs it.

It then recommends the order of what to learn, offers the theory a topic needs right before
it, measures every attempt, and suggests changes to your plan and settings each week for you
to accept or decline. When the shared tracks change in modules you have already started or
finished, it sums the changes up in a few lines at the start of a session and asks once whether
you want them; new material in modules you have not reached yet simply waits for you there. The tutor explains at your level. A complete Python track ships with it
(fundamentals, reading and debugging code, data structures and algorithms, projects, interview
practice). New to the words used here? See [docs/GLOSSARY.md](docs/GLOSSARY.md).

## Why it works

- **Retrieval and spacing.** Every exercise comes back from a blank file after 1, 3, 7, 14, 30
  and 60 days, sooner if it went badly, in a mixed order so you have to recognise each pattern.
- **Start from what you hold.** Each track has a concept graph; a new goal starts with a short
  probe that finds where your understanding ends, so you learn the shortest path to the goal and
  nothing you already know. Every prediction comes with how sure you are, and a confident wrong
  answer is repaired before anything builds on it.
- **Deliberate practice with instant feedback.** Every exercise has tests and a target time;
  time, hints and skipped steps are logged for every attempt.
- **You do the work.** You type every line, run the tests yourself and read the errors before
  the tutor points at anything. Inline AI completion and suggested replies are turned off.
- **Read as much as you write.** Predict, trace, debug and review drills, including spotting
  bugs in AI-written code.
- **New concepts the PRIMM way.** Predict, run, investigate, modify, make: you commit to a
  guess before anything is explained, in a lesson file for that module.
- **Build things.** A ladder of projects with requirements but no step-by-step guide.
- **A method you cannot skip by accident.** Checklists for every activity; the tutor asks you
  to think out loud, flags skipped steps, and the weekly report scores your process.
- **Train the performance, if you need it.** Talk-aloud timed problems and mock interviews, as
  often as your mode says (weekly when preparing for an interview, never unless asked as a hobby).
- **AI as tutor, not ghostwriter.** The evidence and the rules are in [docs/METHOD.md](docs/METHOD.md).

## Quick start

Requires Python 3.10+ (on Windows use `py` or `python`; on macOS and Linux `python3`). Get the
repo (`git clone <this repo> code-dojo`, then `cd code-dojo`), then do **one** of these:

- **In a terminal:** `python dojo.py setup`. It installs what it needs, asks why you are training
  (interview, interview plus growth, entering an industry, or a hobby), the level of programmer
  you want to become, your time per day and your tracks, checks everything, shows the modules
  assigned to you (you can mark any to leave out, with a reason), and tells you exactly what the
  tutor will do next.
- **In the AI tutor:** open `claude` (or `codex`, `gemini`) in the folder and say **set me up**.
  It asks the same questions in the chat, runs the setup for you, then goes straight on to your
  placement: your goals, a short probe of what you already hold, a short practical check, your
  plan, and your modules, which you go
  through together: leave any out or add any back, each with a reason, and decide together.

Either way, everything can be changed later.

Full instructions, the VS Code and Zed debugger setup, voice dictation, using Codex or Gemini,
and moving between machines: [docs/SETUP.md](docs/SETUP.md).

## A session with the tutor

Open the tutor in the repo and say hello. It catches up on what you did without it, tells you
where you stand this week, and proposes today's session from
[docs/DAILY_SESSION.md](docs/DAILY_SESSION.md) (templates from 30 minutes to 3 hours):

1. **Warm-up:** cheat-sheet self-checks or a predict drill.
2. **Redo queue first:** due exercises from a blank file, no peeking at old attempts.
3. **Learn and write:** `teach me <topic>` when a concept is new, then the next exercises.
4. **Read, debug or build:** a bug or review drill, a code-reading exercise, or the project.
5. **Perform** (interview-related modes): an unseen problem under interview conditions, or a
   `mock interview`; in hobby mode this time goes to building.
6. **Log:** mistakes and cheat-sheet lines, then `end of day` for a summary and tomorrow's plan.

Every exercise follows the same loop. Say each step out loud (voice dictation helps):

| Step | You show |
| --- | --- |
| 1. Understand | The task in your own words with the exact condition; clarifying questions |
| 2. Example | A trace by hand of the task's `Trace by hand:` input (no answer printed), plus an edge case of your own |
| 3. Plan | The steps, and the time and space complexity |
| 4. Predict | "Pass" or "test X fails because ...", and how sure you are (0 to 100), then you run the tests yourself |
| 5. Test | Your example and an edge case traced through the finished code |
| 6. Reflect | What would break it, one improvement, names an interviewer would notice |

Things to say: `start <exercise>`, `done <exercise>`, `I'm stuck`, `teach me <topic>`,
`probe me`, `what can I do next`, `bug drill`, `mock interview`, `weekly review`, `end of day`. `TEACHER OFF` turns tutor mode
off until `TEACHER ON`. The full list: [docs/TUTOR.md](docs/TUTOR.md).

## The tracker

The tutor runs `dojo.py` for you, except the tests: those you run and read yourself.

```bash
python dojo.py today                 # time today and this week, redo queue, next exercises
python dojo.py start parse_pairs     # timer + workspace/python/m04_parsing/parse_pairs.py
python dojo.py test parse_pairs      # run the tests against your file
python dojo.py done parse_pairs --hints 1
python dojo.py week --write          # weekly report
python dojo.py graph next            # what you can do now, from the concept graph
```

| Group | Commands |
| --- | --- |
| Set up | `setup` (installs and checks for you), `install`, `doctor` |
| Plan | `today`, `list [module]`, `stats`, `graph [--html]`, `graph next [--goal X]`, `graph path <X>`, `week [--write]`, `mix [track=N ...] [--priority TEXT]`, `settings [key=value ...] [--review]`, `modules` |
| Practise | `start`, `test [--debug]`, `debug <file>` (any exercise, drill, mock or lesson, with editor breakpoints), `done --hints N [--skipped steps] [--confidence N --prediction right\|wrong]`, `pause` / `resume`, `cancel`, `clarify`, `session start\|pause\|resume\|status\|end` (the session clock) |
| Learn | `primm <module> <topic>` (lesson file and timer), `done lesson:<topic>`, `start probe:<track>` / `done probe:<track>`, `log study <minutes> <topic>` |
| Record | `mistake`, `log <kind> <minutes>`, `mark --box N` (things you already know), `graph set` / `graph undo` (concept evidence), `sync` |
| Move data | `export [--to user@host:path \| rclone:gdrive:CodeDojo]` (one zip: your data plus a view of each concept graph), `drive-setup`, `import`, `migrate` |
| Updates | `update` (pull the shared tracks and docs), `changes [--ack]` (what changed in your tracks since you were last asked) |
| Maintain | `verify`, `graph check` |

`python dojo.py help` describes every option.

## What is where

```text
code-dojo/
├── dojo.py                  the tracker's entry point: timers, tests, redo schedule, week balance,
│                            reports, concept graph, export
├── dojolib/                 the tracker's code, one module per area (CONTRIBUTING.md)
├── conftest.py              lets pytest run your workspace file against the track's tests
├── AGENTS.md                tutor-mode rules, shared by Claude Code, Codex and Gemini CLI
├── CLAUDE.md                imports AGENTS.md, plus notes for Claude Code only
├── .agents/skills/          dojo-session, dojo-assess, dojo-probe, dojo-roadmap, dojo-teach,
│                            dojo-mock, dojo-drill, dojo-weekly, dojo-new-exercise, dojo-new-track
│                            (one copy for every tool)
├── .claude/                 Claude Code: settings and start hook, agents (problem-setter,
│                            code-reviewer, progress-coach), skills -> ../.agents/skills
├── .gemini/, .geminiignore  Gemini CLI: reads AGENTS.md, its own agents/; skips the other tools' files
├── .codex/                  Codex: its own agents/ (the same three subagents, in Codex's format)
├── .claude-plugin/          optional: the same skills and agents as a Claude Code plugin
├── .github/                 CODEOWNERS (the owner reviews every change), pull request template,
│                            checks workflow, Dependabot
├── .githooks/, tools/       pre-push checks (tools/check.py: personal data, secrets, syntax, exercises,
│                            concept graphs)
├── CONTRIBUTING.md          how to propose tracks, exercises and fixes
├── SECURITY.md              how to report a security problem privately
├── .vscode/, .zed/          editor and debugger settings, AI completion off
├── docs/                    the method, sessions, tutor commands, setup (see below)
├── tracks/
│   ├── python/              the Python track: README (phases, modules, milestones), graph.json
│   │                        (concept graph), modules (stubs, tests, .clarify/, .solutions/,
│   │                        primm/), projects/
│   ├── cpp/                 placeholder track: prerequisites, theory, outline; built when a plan reaches it
│   ├── django/              placeholder track: prerequisites, theory, outline; built when a plan reaches it
│   └── ros/                 placeholder track: prerequisites, theory, outline; built when a plan reaches it
├── progress/                YOUR data (gitignored): profile, PLAN, BASELINE, log, redo
│                            schedule, concept evidence (graph.json), mistakes, cheat sheet,
│                            weekly reports, mock, drill and probe reports, docs/
├── workspace/               YOUR code (gitignored), mirroring tracks/:
│                            <track>/<module>/ holds your attempts, .history/ (earlier
│                            attempts) and primm/ (lesson files); <track>/drills/<type>/
│                            and <track>/mocks/<type>/ (tests/ and .history/ where needed,
│                            files named by focus), <track>/projects/
└── exports/                 YOUR backups from `dojo.py export`, one zip each (gitignored)
```

## Documentation

| Doc | What it covers |
| --- | --- |
| [SETUP.md](docs/SETUP.md) | Install, the tutor in Claude Code, Codex or Gemini, voice, editors and debugger, moving machines, Google Drive backups |
| [TUTOR.md](docs/TUTOR.md) | Everything you can say to the tutor, and what happens |
| [DAILY_SESSION.md](docs/DAILY_SESSION.md) | Session templates from 30 minutes to 3 hours |
| [CHECKLISTS.md](docs/CHECKLISTS.md) | The method step by step: exercise loop, PRIMM, debugging, reading code, and every practice the tutor enforces |
| [METHOD.md](docs/METHOD.md) | Why it is built this way: the learning research and the rules for AI |
| [INTERVIEW_PLAYBOOK.md](docs/INTERVIEW_PLAYBOOK.md) | The process for live-coding interviews |
| [PERSONAL_DOCS.md](docs/PERSONAL_DOCS.md) | What goes in your own `progress/docs/` and how the tutor keeps it |
| [GLOSSARY.md](docs/GLOSSARY.md) | The words the dojo uses, in plain language |
| [ROADMAP.md](docs/ROADMAP.md) | Choosing tracks, their order and mix from your goals; theory just in time; when the plan changes |
| [TRACKS.md](docs/TRACKS.md) | What is shared and what is personal, and how to add a track or exercises |
| [tracks/python/README.md](tracks/python/README.md) | The Python syllabus: phases, modules, milestones |

## Your data stays yours

`progress/`, `workspace/` and `exports/` never go into git. Back them up or move them with
`python dojo.py export` (a zip), straight to another machine over SSH
(`--to user@host:path`), or to Google Drive (`drive-setup` once, then `export`). Restore with
`python dojo.py import <zip>`.

## Make it yours, or share it

- **Tracks are optional.** Add any subject with a `track.json` and modules; see
  [docs/TRACKS.md](docs/TRACKS.md). Say "design a track for <subject>": the tutor researches the
  best free university courses, official docs and repositories, judges them critically, and
  builds the best course it can: the strongest material as a base, its own judgement for what
  they all miss, and verified, original exercises.
  Every track README says when it was last reviewed and against which version.
- **Friends** get a clean copy (personal data is gitignored), run the quick start, then
  `assess me`: the placement imports what they already know and sets their own plan.
- **Any of three agents.** The rules (`AGENTS.md`) and skills (`.agents/skills/`) exist once
  and serve Claude Code, Codex and Gemini CLI alike; each tool skips the others' files.
- **Plugin (optional).** The skills and agents also install as a Claude Code plugin from this
  repo (`/plugin marketplace add <repo>`, then `/plugin install code-dojo@code-dojo`), for
  example to use the drills and lessons in another project. Inside this repo you do not need
  it: everything loads automatically. Do not install both in the same folder, or each skill
  appears twice.

## Contributing

Changes come in as pull requests, reviewed by the owner before they are merged; see
[CONTRIBUTING.md](CONTRIBUTING.md). `python dojo.py verify` checks that every stub fails and
every reference solution passes; new exercises follow the format in
[docs/TRACKS.md](docs/TRACKS.md).
