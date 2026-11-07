# Contributing

Thank you for helping. Every change reaches `main` through a pull request that the owner
reviews; nobody else can push to `main` directly.

## How

1. Fork the repository and create a branch.
2. Make the change, then check it:
   - exercises: `python dojo.py verify <slugs>` (the stub must fail, the reference must pass);
   - tracker: run the commands you touched, and `python dojo.py doctor`.
3. Open a pull request and fill in its checklist.

## What fits

- **Tracks and exercises** in the format of `docs/TRACKS.md` (task, tests, reference solution,
  clarify file), verified.
- **Docs, skills and agents** that work for any learner, at any level and in any mode.
- **Tracker fixes and features** in `dojo.py`, plain Python 3.10+, no new dependencies without a
  reason.

## What does not

- Personal data of any kind: `progress/`, `workspace/` and `exports/` are gitignored for a
  reason. Anything about one learner belongs in their own `progress/docs/`
  (`docs/PERSONAL_DOCS.md`).
- Time estimates in shared files: they depend on the learner and live in their `PLAN.md`.
- Changes that let the tutor write a learner's exercise code (`AGENTS.md`, hard rules).
