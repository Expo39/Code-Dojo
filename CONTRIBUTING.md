# Contributing

Thank you for helping. Every change reaches `main` through a pull request that the owner
reviews; nobody else can push to `main` directly.

## How

1. Fork the repository and create a branch.
2. Make the change, then check it: `python tools/check.py` (no personal data, no secrets, Python
   compiles, JSON parses, changed exercises verify). After `python dojo.py setup` or `doctor` it
   also runs by itself before every push. Run the commands you touched, too.
3. Open a pull request and fill in its checklist. The same checks, plus `dojo.py verify` on every
   exercise, run on GitHub; the owner approves running them for outside contributors.

## What fits

- **Tracks and exercises** in the format of `docs/TRACKS.md` (task, tests, reference solution,
  clarify file), verified and original. Improve an existing exercise, or let one exercise train
  two topics, before adding a new one: more exercises are not a better track. A new track starts from research into the best current
  free courses and docs (`dojo-new-track`) and lists its sources and review date in its README.
- **Docs, skills and agents** that work for any learner, at any level and in any mode. A subagent
  exists for each tool (`.claude/agents/`, `.codex/agents/`, `.gemini/agents/`): change all three
  together; the checks compare them.
- **Tracker fixes and features** in `dojo.py`, plain Python 3.10+, no new dependencies without a
  reason.

Everything you write follows the conventions in `AGENTS.md` (Style): British English; dates
DD/MM/YYYY (DD-MM-YYYY in file names, DD_MM_YYYY in identifiers); 24-hour time; weeks from
Monday; euros; metric and SI units. Anything generated on the spot (drills, mocks) goes in a type
folder named by its focus, with its own tests and `.history/` where the kind needs them.

## What does not

- Personal data of any kind: `progress/`, `workspace/` and `exports/` are gitignored for a
  reason. Anything about one learner belongs in their own `progress/docs/`
  (`docs/PERSONAL_DOCS.md`).
- Time estimates in shared files: they depend on the learner and live in their `PLAN.md`.
- Changes that let the tutor write a learner's exercise code (`AGENTS.md`, hard rules).
- Code that reaches the network or runs commands without the learner's say: changes to
  `dojo.py`, `conftest.py`, tests, `track.json` test commands, hooks and workflows get the
  closest review. Report security problems privately: `SECURITY.md`.
