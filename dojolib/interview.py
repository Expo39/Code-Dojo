"""The interview checklist (docs/CHECKLISTS.md, section 8): what the learner wants to prepare for
one interview, worked through item by item, with a parking lot for everything else."""

from __future__ import annotations

import re
from pathlib import Path

from .core import PROFILE, PROGRESS, die, fmt_date, load_profile, parse_date, today, write_json

INTERVIEWS = PROGRESS / "interviews"
TEMPLATE = """# Interview: {name}

Date: {date}
Format: (discussion, live coding, take-home)

## Items

One line per item: `- [ ] topic | how it is practised (read, drill, mock) | done when <observable bar>`.
The learner agrees each line; the tutor adds none without their say.

## Out of scope

## Parking lot

One line per tangent that came up while working through the items; offered after the interview.
"""
ITEM = re.compile(r"^- \[( |x)\] (.+)$")


def active_file(profile: dict) -> Path | None:
    """The checklist of the interview now set up, or None."""
    stem = profile.get("interview")
    path = INTERVIEWS / f"{stem}.md" if stem else None
    return path if path and path.exists() else None


def read_items(path: Path) -> list[tuple[bool, str]]:
    """The (done, text) of every item under '## Items'."""
    items, inside = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Items"
        elif inside and (m := ITEM.match(line.strip())):
            items.append((m.group(1) == "x", m.group(2)))
    return items


def mark_done(path: Path, n: int) -> None:
    """Tick the n-th item (counting from 1) under '## Items'."""
    lines, inside, seen = path.read_text(encoding="utf-8").splitlines(), False, 0
    for i, line in enumerate(lines):
        if line.startswith("## "):
            inside = line.strip() == "## Items"
        elif inside and ITEM.match(line.strip()):
            seen += 1
            if seen == n:
                lines[i] = line.replace("- [ ]", "- [x]", 1)
                break
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parking_lot(path: Path) -> list[str]:
    lines, inside = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Parking lot"
        elif inside and line.startswith("- "):
            lines.append(line[2:])
    return lines


def interview_line(profile: dict, on) -> str | None:
    """The line `today` prints: progress while it is coming, a close-out reminder once it has passed."""
    path = active_file(profile)
    if not path:
        return None
    items = read_items(path)
    done = sum(1 for d, _ in items if d)
    when = profile.get("sprint_until")
    days = (parse_date(when) - on).days if when else None
    if days is not None and days < 0:
        return (f"Interview {path.stem} has passed: close it out (`python3 dojo.py interview close`), "
                "then choose the mode and replan (dojo-roadmap). Nothing else is owed.")
    left = [t for d, t in items if not d]
    nxt = f"next: {left[0].split('|')[0].strip()}" if left else "all items done"
    return (f"Interview checklist {path.stem}"
            + (f", {days} days left" if days is not None else "")
            + f": {done} of {len(items)} items done, {nxt}. Work only on these items; a tangent goes "
              "to the parking lot (`python3 dojo.py interview park \"...\"`), never into the session.")


def cmd_interview(args) -> None:
    profile = load_profile()
    action = args.action or "status"
    if action == "start":
        if not args.rest or len(args.rest) != 2:
            die('Use: interview start <name> <DD/MM/YYYY>   (for example: interview start ai_at_work 25/11/2026)')
        name, date_text = args.rest
        parse_date(date_text)
        INTERVIEWS.mkdir(parents=True, exist_ok=True)
        stem = f"{date_text.replace('/', '-')}_{name}"
        path = INTERVIEWS / f"{stem}.md"
        if not path.exists():
            path.write_text(TEMPLATE.format(name=name, date=date_text), encoding="utf-8")
        profile["interview"] = stem
        profile["sprint_until"] = date_text
        write_json(PROFILE, profile)
        print(f"Checklist: {path.relative_to(PROGRESS.parent)}. Fill the items with the learner "
              "(dojo-interview-prep), and note it under 'Plan changes' in progress/PLAN.md.")
        return
    path = active_file(profile)
    if not path:
        die("No interview checklist is set up. Start one: interview start <name> <DD/MM/YYYY>")
    if action == "status":
        items = read_items(path)
        print(f"{path.stem}: {sum(1 for d, _ in items if d)} of {len(items)} items done")
        for n, (done, text) in enumerate(items, 1):
            print(f"  {n}. [{'x' if done else ' '}] {text}")
        lot = parking_lot(path)
        print(f"Parking lot ({len(lot)}): " + ("; ".join(lot) if lot else "empty"))
    elif action == "check":
        if len(args.rest) != 1 or not args.rest[0].isdigit():
            die("Use: interview check <item number> (numbers from `interview status`)")
        n = int(args.rest[0])
        items = read_items(path)
        if not 1 <= n <= len(items):
            die(f"No item {n}: the checklist has {len(items)}.")
        mark_done(path, n)
        print(f"Item {n} done: {items[n - 1][1].split('|')[0].strip()}")
    elif action == "park":
        if not args.rest:
            die('Use: interview park "<one line about the tangent>"')
        text = " ".join(args.rest).strip()
        content = path.read_text(encoding="utf-8").rstrip("\n") + f"\n- {fmt_date(today())}: {text}\n"
        path.write_text(content, encoding="utf-8")
        print("Parked. It is offered after the interview, not before.")
    elif action == "close":
        done_dir = INTERVIEWS / "done"
        done_dir.mkdir(parents=True, exist_ok=True)
        path.rename(done_dir / path.name)
        for key in ("interview", "sprint_until", "priority"):
            profile[key] = ""
        write_json(PROFILE, profile)
        print(f"Closed and archived in progress/interviews/done/. The sprint and the priority are cleared.\n"
              "Next: say whether to keep training for interviews or not, then `python3 dojo.py mode <x>` "
              "and a replan (dojo-roadmap); the parking lot is the first thing to offer.")
    else:
        die("interview: start, status, check, park or close.")
