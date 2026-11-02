# Setup (Windows, macOS, Linux)

Everything runs on plain Python 3.10 or newer. No shell scripts, no symlinks, no OS-specific
steps beyond the Python command name.

| | Windows | macOS / Linux |
| --- | --- | --- |
| Python command | `py` or `python` | `python3` |
| Install Python | python.org installer (tick "Add python.exe to PATH") or `winget install Python.Python.3.13` | macOS: python.org or Homebrew. Linux: your package manager (e.g. `sudo apt install python3 python3-venv`) |

In the commands below, replace `python` with what your system uses.

## First time

```bash
git clone <your fork or copy of this repo> code-dojo
cd code-dojo
python dojo.py install
python dojo.py setup
python dojo.py doctor
```

`install` creates `.venv` and installs pytest into it; you do not need to activate it, because
`dojo.py` finds it itself. `setup` asks for your name, time per weekday, rest days, an optional
target date, your tracks and your level.

## Claude Code (the tutor)

Install Claude Code (https://claude.com/claude-code), open a terminal in the repo and run
`claude`. The tutor rules in `CLAUDE.md`, the skills in `.claude/skills/` and the agents in
`.claude/agents/` load automatically; nothing else to install. At the start of each session a
hook prints your status (`python dojo.py brief`) so the tutor knows where you are.

On Windows, Claude Code needs Git for Windows (it runs hooks through Git Bash); install it
from https://git-scm.com if you do not have it.

## Editor and debugger (VS Code recommended)

1. Install VS Code and the Python extension.
2. Open the repo folder; choose `.venv` as the interpreter when asked (Ctrl+Shift+P, then
   "Python: Select Interpreter").
3. **Turn off AI completion** for this folder (Copilot or similar): the point is to type it
   yourself. The repo's `.vscode/settings.json` already disables inline suggestions here.
4. Debugging a failing exercise: open `workspace/python/<exercise>.py`, set a breakpoint
   (click left of a line number), then Run and Debug (Ctrl+Shift+D) and pick
   "Debug: current exercise's tests". It runs that exercise's tests and stops at your
   breakpoint.

| Debugger action | Key |
| --- | --- |
| Breakpoint | F9 |
| Start / continue | F5 |
| Step over / into / out | F10 / F11 / Shift+F11 |
| Run any expression while paused | Debug Console |

Without VS Code: put `breakpoint()` on a line and run the test; then `n` next, `s` step into,
`p name` print, `c` continue, `q` quit.

## Moving to another machine

```bash
python dojo.py export --to user@other-machine:~/
```

On the other machine: `python dojo.py import ~/code-dojo_<name>_<date>.zip`. Set a default
target in `progress/profile.json` (`"export_target": "user@host:path"`) to just run
`python dojo.py export`. `scp` comes with OpenSSH, which is built into Windows 10 and later,
macOS and most Linux distributions.

## Sharing with a friend

Give them the repository (or let them fork it). Your personal data is gitignored, so they get
a clean copy. They run the "First time" steps above, then `/dojo-assess` in Claude Code.
