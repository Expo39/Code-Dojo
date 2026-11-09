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
python dojo.py setup
```

`setup` is the only command to run. It creates `.venv` with pytest if it is missing (you never
need to activate it: `dojo.py` finds it), asks your name, mode (interview, hybrid, industry,
hobby), target level, time per weekday and rest days, an optional target date, your tracks and
your level, runs the checks (`doctor`, which also turns on the pre-push checks used when you
change the shared files: `tools/check.py`), shows the modules assigned to you (mark any you want to
leave out, with a reason the tutor discusses with you later), and ends with what the tutor will
do next. Or skip the
terminal: open the tutor and say "set me up"; it asks in the chat and runs `setup` for you.

## Claude Code (the tutor)

Install Claude Code (https://claude.com/claude-code), open a terminal in the repo and run
`claude`. The tutor rules (`CLAUDE.md`, which imports `AGENTS.md`), the skills in
`.agents/skills/` (through the `.claude/skills` link) and the agents in `.claude/agents/` load
automatically; nothing else to install. At the start of each session a
hook prints your status (`python dojo.py brief`) so the tutor knows where you are.

Recommended: turn on voice dictation with `/voice` in Claude Code, then hold the spacebar to
talk (the dictation language is set in `/config`). Speaking the restate, trace and plan steps
is faster than typing them and closer to a real interview. See "Talk, do not type" in
`TUTOR.md`. On Linux it needs microphone access and may ask for an audio recorder such as SoX.

On Windows, Claude Code needs Git for Windows (it runs hooks through Git Bash); install it
from https://git-scm.com if you do not have it.

## Codex or Gemini CLI (alternative tutors)

The tutor also runs in OpenAI Codex and Google Gemini CLI. All three tools share one set of
rules, `AGENTS.md`, and one copy of the skills, `.agents/skills/`, so a fix to the method
reaches every tool. Each tool is told to skip the others' files (the "Files per tool" table in
`AGENTS.md`), so none spends time rereading the same rules.

- **Codex:** run `codex` in the repo. It reads `AGENTS.md`, its subagents in `.codex/agents/`, and discovers `.agents/skills/` on
  its own.
- **Gemini CLI:** run `gemini` in the repo. It uses its subagents in `.gemini/agents/`; `.gemini/settings.json` points it at `AGENTS.md`
  instead of `GEMINI.md`, and `.geminiignore` hides the Claude Code files from it.

Differences from Claude Code: there is no session-start hook, so the tutor runs
`python dojo.py brief` itself on your first message. The three subagents (problem-setter,
code-reviewer, progress-coach) exist for each tool, in its own folder and format, and say the
same thing (the pre-push check compares them). Turn off any suggested
replies or inline completions the tool offers, as Claude Code's are here.

**Symlinks on Windows.** `.claude/skills` is a link to `.agents/skills`. If your Git checkout
does not create symlinks, `python dojo.py setup` (or `doctor`) replaces it with a link or, if
that is not allowed, a copy.

## Editor and debugger: VS Code or Zed

Both are configured in the repo (`.vscode/` and `.zed/`). In both, inline AI suggestions are
off for this folder (the point is to type it yourself) and the `.solutions/` and `.clarify/`
folders are hidden from the file panel. Autosave is on in both, so `python dojo.py test` always
runs what you see on screen (the tracker also warns if your file is still the untouched stub).

The debugger runs `python dojo.py debug <file>` on the file you have open, inside the debugger's
own process, so breakpoints in your `workspace/` file are hit: an exercise runs its tests, a drill
or mock (`drills/<type>/`, `mocks/<type>/`) the test file in its type folder, and anything else,
such as a lesson file, runs as a script. Python tracks only; other languages use their own tools.

### VS Code

1. Install VS Code and the Python extension; open the repo folder.
2. Choose `.venv` as the interpreter (Ctrl+Shift+P, "Python: Select Interpreter").
3. Turn off Copilot or any other AI completion for this folder if it is still active.
4. To debug: open the file (an exercise, a drill, a mock or a lesson), set a breakpoint (click left
   of a line number or F9), open Run and Debug (Ctrl+Shift+D) and start "Debug: this file".

### Zed

1. Open the repo folder. Zed detects `.venv` automatically (check the toolchain selector in the
   status bar shows `.venv`).
2. Edit predictions are turned off for this project in `.zed/settings.json`. If you use Zed's
   agent panel, do not ask it for exercise code: the tutor runs in Claude Code.
3. To debug: open the file (an exercise, a drill, a mock or a lesson), set a breakpoint (click the
   gutter left of a line), press F4 (or "debugger: start" in the command palette) and pick
   "Debug: this file".
4. Tasks (command palette, "task: spawn"): `dojo: today`, `dojo: start current exercise`,
   `dojo: test current exercise`, `dojo: list exercises`. On Windows use the "(Windows)"
   variants, which call `python` instead of `python3`.

### Debugger keys

| Action | VS Code | Zed |
| --- | --- | --- |
| Toggle breakpoint | F9 | click the gutter (or the "editor: toggle breakpoint" command) |
| Start / continue | F5 | F4 to start, then the debug panel's continue button |
| Step over / into / out | F10 / F11 / Shift+F11 | the debug panel's step buttons |
| Inspect values | Variables and Watch panels, hover | the debug panel's variables view, hover |

"Debug: this file" runs `dojo.py debug <file>`: an exercise runs its tests, a drill or mock the
test file in its `tests/` folder (as does an open test file), anything else runs as a script.

Without an editor debugger: put `breakpoint()` on a line and run `python dojo.py debug <file>` in a
terminal (not through Claude Code's `!`, which cannot take typed input);
then `n` next, `s` step into, `p name` print, `c` continue, `q` quit.

## Getting updates

Tracks, exercises and docs keep improving. Once a day, the session start checks the shared
repository and tells you when there are updates; say `update` to the tutor, or run
`python dojo.py update`. It first shows the incoming changes and which of the changed files run
code on your machine (the tracker, tests, hooks), and applies them only after your yes; your
`progress/` and `workspace/` are never touched. Then it lists what changed in modules you have
already started or finished, and you choose to learn it, mark it as already known, or leave it
out (all at once or one by one). Changes in modules you have not reached yet need no answer:
you meet them there. `python dojo.py changes` shows the list again at any time. If you work from a fork, add the original as a remote named `upstream`
(`git remote add upstream <url>`); `update` pulls from it.

## Moving to another machine

```bash
python dojo.py export --to user@other-machine:~/
```

The zip holds `progress/` and `workspace/` (your concept evidence and probe reports included)
and, in the same zip, `views/` with a current page of each concept graph that opens in any
browser. On the other machine: `python dojo.py import ~/code-dojo_<name>_<date>.zip` (it restores
your data; the views are made fresh whenever you ask). Set a default
target once (`python dojo.py settings export_target=user@host:path`) to just run
`python dojo.py export`. `scp` comes with OpenSSH, which is built into Windows 10 and later,
macOS and most Linux distributions.

### Google Drive

```bash
python dojo.py drive-setup     # once: sign in to Google, saves the export target
python dojo.py export          # zips and uploads to the CodeDojo folder in your Drive
```

It uses rclone: the one on your PATH if you have it, otherwise the `rclone/rclone` Docker
image (pulled automatically; config in `~/.config/rclone`). The sign-in asks only for access
to files rclone itself creates (`drive.file`), not your whole Drive. Options:
`--remote <name>` and `--folder <folder>`; `export --to rclone:<remote>:<folder>` for a one-off.
On the other machine, download the zip from Drive and run `python dojo.py import <zip>`.

## Sharing with a friend

Give them the repository (or let them fork it). Your personal data is gitignored, so they get
a clean copy. They run `python dojo.py setup` (or say "set me up" to the tutor), then
`assess me`.
