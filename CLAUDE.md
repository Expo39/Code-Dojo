@AGENTS.md

## Claude Code only

- The SessionStart hook in `.claude/settings.json` prints `[dojo status ...]`; you do not need
  to run `dojo.py brief` yourself when that block is present.
- Skills load from `.claude/skills`, a link to `.agents/skills`. If it is missing or broken
  (a Windows checkout without symlinks), `python dojo.py doctor` repairs it.
- Run the agents in `.claude/agents/` with the Agent tool.
- Prompt suggestions are off for this project (`promptSuggestionEnabled` in
  `.claude/settings.json`), so the learner never sees a suggested answer in the input box.
- Skip `.gemini/`, `.geminiignore` and `.codex/`: they configure other tools.
