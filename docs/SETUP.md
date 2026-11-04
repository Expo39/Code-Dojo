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

Recommended: turn on voice dictation with `/voice` in Claude Code, then hold the spacebar to
talk (the dictation language is set in `/config`). Speaking the restate, trace and plan steps
is faster than typing them and closer to a real interview. See "Talk, do not type" in
`TUTOR.md`. On Linux it needs microphone access and may ask for an audio recorder such as SoX.

On Windows, Claude Code needs Git for Windows (it runs hooks through Git Bash); install it
from https://git-scm.com if you do not have it.

## Editor and debugger: VS Code or Zed

Both are configured in the repo (`.vscode/` and `.zed/`). In both, inline AI suggestions are
off for this folder (the point is to type it yourself) and the `.solutions/` and `.clarify/`
folders are hidden from the file panel. Autosave is on in both, so `python dojo.py test` always
runs what you see on screen (the tracker also warns if your file is still the untouched stub).

The debugger always runs `python dojo.py test <exercise> --debug`, which runs that exercise's
tests inside the debugger's own process, so breakpoints in your `workspace/` file are hit.

### VS Code

1. Install VS Code and the Python extension; open the repo folder.
2. Choose `.venv` as the interpreter (Ctrl+Shift+P, "Python: Select Interpreter").
3. Turn off Copilot or any other AI completion for this folder if it is still active.
4. To debug: open `workspace/python/<exercise>.py`, set a breakpoint (click left of a line
   number or F9), open Run and Debug (Ctrl+Shift+D) and start "Debug: current exercise's tests".

### Zed

1. Open the repo folder. Zed detects `.venv` automatically (check the toolchain selector in the
   status bar shows `.venv`).
2. Edit predictions are turned off for this project in `.zed/settings.json`. If you use Zed's
   agent panel, do not ask it for exercise code: the tutor runs in Claude Code.
3. To debug: open `workspace/python/<exercise>.py`, set a breakpoint (click the gutter left of a
   line), press F4 (or "debugger: start" in the command palette) and pick
   "Debug: current exercise's tests".
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

Without an editor debugger: put `breakpoint()` on a line and run `python dojo.py test <exercise>`;
then `n` next, `s` step into, `p name` print, `c` continue, `q` quit.

## Moving to another machine

```bash
python dojo.py export --to user@other-machine:~/
```

On the other machine: `python dojo.py import ~/code-dojo_<name>_<date>.zip`. Set a default
target in `progress/profile.json` (`"export_target": "user@host:path"`) to just run
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
a clean copy. They run the "First time" steps above, then `/dojo-assess` in Claude Code.
