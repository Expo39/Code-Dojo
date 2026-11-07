@AGENTS.md

## Claude Code only

- When the `[dojo status ...]` block from the SessionStart hook is present, do not run
  `dojo.py brief` again.
- Skills load through the `.claude/skills` link; if it is missing or broken, `python dojo.py doctor`
  repairs it. Run the agents in `.claude/agents/` with the Agent tool.
