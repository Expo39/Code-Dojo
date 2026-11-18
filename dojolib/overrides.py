"""Personal overrides: rules that replace a shared rule for this learner only.

They live in progress/overrides.md (personal, gitignored), one per line:

    - DD/MM/YYYY | <file> > <section> | <the rule as it applies to this learner>

The brief prints them, so every tool sees them at session start; `dojo.py overrides` lists them
and flags a location whose file no longer exists.
"""

from __future__ import annotations

from .core import PROGRESS, ROOT

OVERRIDES = PROGRESS / "overrides.md"

HEADER = """# My overrides

Personal and local (gitignored). Rules that replace a shared rule (AGENTS.md, docs/, a skill)
for me only; they win over the shared file. One per line, newest first:

    - DD/MM/YYYY | <file> > <section> | <the rule as it applies to me>

A change that would suit every learner goes in the shared file instead.

"""


def read_overrides() -> list[dict]:
    """Every well-formed override line, in file order."""
    if not OVERRIDES.exists():
        return []
    rules = []
    for line in OVERRIDES.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- "):
            continue
        parts = [p.strip() for p in line[2:].split("|", 2)]
        if len(parts) != 3 or not all(parts):
            continue
        date, where, rule = parts
        rules.append({"date": date, "where": where, "file": where.split(">")[0].strip(), "rule": rule})
    return rules


def overrides_line() -> str:
    """One status line naming every override, or "" when there are none."""
    rules = read_overrides()
    if not rules:
        return ""
    return (f"Overrides ({len(rules)}, progress/overrides.md, these win over the shared rules): "
            + " | ".join(f"{r['where']}: {r['rule']}" for r in rules))


def cmd_overrides(args) -> None:
    if not OVERRIDES.exists():
        OVERRIDES.parent.mkdir(parents=True, exist_ok=True)
        OVERRIDES.write_text(HEADER, encoding="utf-8")
        print("Created progress/overrides.md: add one line per rule:\n"
              "  - DD/MM/YYYY | <file> > <section> | <the rule as it applies to you>")
        return
    rules = read_overrides()
    if not rules:
        print("progress/overrides.md has no override lines yet.")
    for r in rules:
        missing = "" if (ROOT / r["file"]).exists() else f"  [{r['file']} not found: check the location]"
        print(f"{r['date']}  {r['where']}\n    {r['rule']}{missing}")
