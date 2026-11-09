"""Shared-repo updates and track changes the learner has not been asked about yet."""

from __future__ import annotations

import argparse
import subprocess
import sys

from .core import (
    PROFILE, PROGRESS, REVIEWS, ROOT, SEEN, TOPICS_SEEN, UPSTREAM_CHECK, ask, die, fmt_date,
    load_profile, read_json, today, write_json
)
from .tracks import discover, exercise_hash, module_topics, skipped_module, started_modules


def topic_changes() -> dict:
    """New lesson topics per module since the learner was last asked (modules they skip stay quiet)."""
    current = module_topics()
    if not TOPICS_SEEN.exists():
        if PROFILE.exists():
            write_json(TOPICS_SEEN, current)
        return {}
    seen = read_json(TOPICS_SEEN, {})
    profile = read_json(PROFILE, {})
    started = started_modules()
    out = {}
    for module in sorted(set(current) | set(seen)):
        if skipped_module(module, profile) or module.split("/")[-1] not in started:
            if module in current and seen.get(module) != current[module]:
                seen[module] = current[module]  # recorded silently: met when the module is reached
                write_json(TOPICS_SEEN, seen)
            continue
        new = [t for t in current.get(module, []) if t not in seen.get(module, [])]
        gone = [t for t in seen.get(module, []) if t not in current.get(module, [])]
        # "default arguments" -> "default and keyword arguments" is a rewording, not a removal
        reworded = [(g, n) for g in gone for n in new
                    if all(w in n.lower() for w in g.lower().split())]
        new = [n for n in new if n not in {r[1] for r in reworded}] + \
              [f"{n} (was: {g})" for g, n in reworded if n != g and any(w not in g.lower() for w in n.lower().split())]
        gone = [g for g in gone if g not in {r[0] for r in reworded}]
        if new or gone:
            out[module] = {"new": new, "removed": gone}
    return out


def track_changes() -> dict:
    """New, changed and removed exercises in the learner's tracks since they were last asked.
    The first run records everything as seen, so a new learner is not asked about every exercise."""
    current = {slug: exercise_hash(ex) for slug, ex in discover().items()}
    if not SEEN.exists():
        if PROFILE.exists():
            write_json(SEEN, current)
        return {"new": [], "changed": [], "removed": [], "topics": topic_changes()}
    seen = read_json(SEEN, {})
    profile = read_json(PROFILE, {})
    exercises = discover()
    started = started_modules()
    quiet = {sl for sl, ex in exercises.items()
             if skipped_module(ex["module"], profile) or ex["module"] not in started}
    silent = {sl: current[sl] for sl in quiet if seen.get(sl) != current[sl]}
    if silent:  # nothing to ask: new material in an unreached module is met there
        seen.update(silent)
        write_json(SEEN, seen)
    return {"new": [s for s in current if s not in seen and s not in quiet],
            "changed": [s for s in current if s in seen and seen[s] != current[s] and s not in quiet],
            "removed": [s for s in seen if s not in current],
            "topics": topic_changes()}


def acknowledge_changes(slugs: list[str] | None = None) -> None:
    current = {slug: exercise_hash(ex) for slug, ex in discover().items()}
    seen = read_json(SEEN, {})
    reviews = read_json(REVIEWS, {})
    for slug in (slugs or list(current) + list(seen)):
        if slug in current:
            seen[slug] = current[slug]
        else:
            seen.pop(slug, None)
            reviews.pop(slug, None)  # the exercise is gone; its history stays in the log
    write_json(SEEN, seen)
    write_json(REVIEWS, reviews)
    if not slugs:  # acknowledging everything includes the lesson topics
        write_json(TOPICS_SEEN, module_topics())


def changes_lines(changes: dict) -> list[str]:
    exercises = discover()
    lines = []
    topics = changes.get("topics", {})
    for kind in ("new", "removed"):
        parts = [f"{m} ({', '.join(t[kind])})" for m, t in topics.items() if t[kind]]
        if parts:
            lines.append(f"{kind} lesson topics: " + "; ".join(parts))
    for kind in ("new", "changed", "removed"):
        if not changes[kind]:
            continue
        if kind == "removed":
            lines.append(f"{len(changes[kind])} removed exercise(s): {', '.join(changes[kind])} "
                         "(recording them as seen drops them from your redo schedule)")
            continue
        by_module: dict[str, list[str]] = {}
        for slug in changes[kind]:
            module = f"{exercises[slug]['track']}/{exercises[slug]['module']}" if slug in exercises else "?"
            by_module.setdefault(module, []).append(slug)
        lines.append(f"{len(changes[kind])} {kind}: " + "; ".join(
            f"{m} ({', '.join(sl)})" for m, sl in by_module.items()))
    return lines


def upstream_remote() -> str:
    names = subprocess.run(["git", "-C", str(ROOT), "remote"], capture_output=True, text=True).stdout.split()
    return "upstream" if "upstream" in names else ("origin" if "origin" in names else "")


def upstream_behind(fetch: bool) -> int | None:
    """Commits on the shared repo's main branch that this copy does not have (None = unknown)."""
    remote = upstream_remote()
    if not remote:
        return None
    if fetch:
        try:
            subprocess.run(["git", "-C", str(ROOT), "fetch", "--quiet", remote],
                           capture_output=True, timeout=8)
        except (subprocess.TimeoutExpired, OSError):
            return None
    branch = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--abbrev-ref", f"{remote}/HEAD"],
                            capture_output=True, text=True).stdout.strip() or f"{remote}/main"
    out = subprocess.run(["git", "-C", str(ROOT), "rev-list", "--count", f"HEAD..{branch}"],
                         capture_output=True, text=True)
    return int(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip().isdigit() else None


def daily_upstream_check() -> int | None:
    """At most one network check a day, so session start stays fast."""
    state = read_json(UPSTREAM_CHECK, {})
    if state.get("date") == fmt_date(today()):
        return state.get("behind")
    behind = upstream_behind(fetch=True)
    if PROGRESS.exists():
        write_json(UPSTREAM_CHECK, {"date": fmt_date(today()), "behind": behind})
    return behind


def cmd_changes(args) -> None:
    """Show track changes since the learner was last asked; --ack records them as seen."""
    load_profile()
    if args.ack is not None:
        acknowledge_changes(args.ack or None)
        print("Recorded as seen" + (f": {', '.join(args.ack)}." if args.ack else ": all current changes."))
        return
    lines = changes_lines(track_changes())
    if not lines:
        print("No track changes since you were last asked.")
        return
    print("Track changes since you were last asked:")
    for line in lines:
        print("  " + line)
    print("For each new or changed exercise: learn it (nothing to do), already know it "
          "(`mark <slug> --box 3`), or not for me (`settings skip_exercises+=<slug>`, or skip_modules+=<module>).")
    print("For a changed exercise: redo the new version (nothing to do), already know it "
          "(`mark <slug> --box 3`), or leave it out (`settings skip_exercises+=<slug>`).")
    print("For new lesson topics: learn it (`teach me <topic>`, now or when that module comes up), "
          "already know it, or not for me. Removed exercises and topics: tell the learner, then acknowledge.")
    print("Then: python dojo.py changes --ack [slugs]")


def cmd_update(args) -> None:
    """Pull the shared repo's latest tracks and docs, then show what changed in your tracks."""
    remote = upstream_remote()
    if not remote:
        die("No git remote found: this copy cannot be updated with git.")
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=no"],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        die("You have local changes to shared files (git status shows them). Commit or stash them, "
            "then run update again.")
    branch = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "-C", str(ROOT), "fetch", "--quiet", remote, branch])
    incoming = f"HEAD..{remote}/{branch}"
    log = subprocess.run(["git", "-C", str(ROOT), "log", "--oneline", incoming],
                         capture_output=True, text=True).stdout.strip()
    if not log:
        print("Already up to date.")
        write_json(UPSTREAM_CHECK, {"date": fmt_date(today()), "behind": 0})
        cmd_changes(argparse.Namespace(ack=None))
        return
    files = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", incoming],
                           capture_output=True, text=True).stdout.split()
    runs = [f for f in files if f.endswith((".py", ".sh", "track.json"))
            or f.startswith((".claude/", ".githooks/", ".github/", "dojolib/"))]  # graph_view.html runs in your browser
    print(f"Incoming from {remote}/{branch}:\n" + "\n".join("  " + line for line in log.splitlines()))
    print(f"{len(files)} file(s) change" + (f"; these run on your machine, so they are worth a look "
          f"(git diff {incoming} -- <file>):\n  " + "\n  ".join(runs) if runs else "."))
    if not args.yes:
        if not sys.stdin.isatty():
            die("Run `python dojo.py update --yes` to apply them.")
        if not ask("Apply them? (y/n)", "y").lower().startswith("y"):
            print("Nothing changed.")
            return
    result = subprocess.run(["git", "-C", str(ROOT), "merge", "--ff-only", f"{remote}/{branch}"])
    if result.returncode != 0:
        die("The update could not be applied automatically (see the git message above).")
    write_json(UPSTREAM_CHECK, {"date": fmt_date(today()), "behind": 0})
    cmd_changes(argparse.Namespace(ack=None))
