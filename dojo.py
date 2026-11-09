#!/usr/bin/env python3
"""Code Dojo: tracker, scheduler and exercise runner.

Standard library only, works on Linux, macOS and Windows.
Run `python dojo.py help` for the commands (use `python3` on Linux/macOS if
`python` is not found). This file is the entry point that every command, editor task and hook
calls; the code lives in dojolib/, one module per area (CONTRIBUTING.md lists them).
"""

from dojolib.cli import main

if __name__ == "__main__":
    main()
