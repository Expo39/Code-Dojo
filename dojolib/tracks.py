"""Tracks and exercises: discovery, running tests, lesson topics, and the workspace layout."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

from .core import (
    HISTORY_DIR, PRIMM_DIR, REVIEWS, ROOT, TARGETS, TRACKS, TRACKS_PERSONAL, WORKSPACE, active_track_names, die,
    read_json
)


HEADER_RE = re.compile(r"^\s*(?:#|//|--|\*|;)?\s*(Level|Target|Pattern|Kind|Variant of):\s*(.+?)\s*$", re.MULTILINE)
STUB_RE = re.compile(r"^[a-z]\d\d_([a-z0-9_]+)(\.[A-Za-z0-9]+)$")
DEFAULT_TRACK = {
    "name": "",
    "extension": ".py",
    "test_file": "tests/test_{slug}.py",
    "solution_file": ".solutions/{slug}.py",
    "clarify_file": ".clarify/{slug}.md",
    "test_command": None,
    # What a learner should have before starting this track, in words (docs/ROADMAP.md).
    "requires": [],
    # When the track was last checked against current courses and the current version (DD/MM/YYYY).
    "reviewed": "",
    # The tracks this one builds on (pandas and django on python; ros on cpp and python): shown
    # beside its name, so a family of tracks reads together without nesting folders.
    "builds_on": [],
}


def load_tracks(active_only: bool = True) -> dict:
    """Map track folder name -> its track.json settings, from tracks/ (shared) and
    tracks_personal/ (the learner's own, gitignored). A personal track with the name of a shared
    one is left out (doctor reports it)."""
    tracks = {}
    for root, personal in ((TRACKS, False), (TRACKS_PERSONAL, True)):
        for config in sorted(root.glob("*/track.json")):
            if config.parent.name in tracks:
                continue
            settings = dict(DEFAULT_TRACK)
            settings.update(read_json(config, {}))
            settings["dir"] = config.parent
            settings["name"] = settings["name"] or config.parent.name
            settings["personal"] = personal
            tracks[config.parent.name] = settings
    if active_only:
        chosen = set(active_track_names())
        tracks = {k: v for k, v in tracks.items() if k in chosen}
    return tracks


def track_heading(name: str, track: dict | None = None) -> str:
    """A track's name with the tracks it builds on, e.g. "pandas (builds on python)"."""
    if track is None:
        track = load_tracks(active_only=False).get(name, {})
    parents = track.get("builds_on") or []
    label = f"{name} (personal)" if track.get("personal") else name
    return f"{label} (builds on {', '.join(parents)})" if parents else label


def discover(active_only: bool = True) -> dict:
    """Map slug -> exercise metadata, in syllabus order, for the learner's tracks.

    Layout: tracks/<track>/<module>/<original>/ holds one exercise (<prefix>NN_<slug>.<ext>) and
    its variants (vNN_<slug>.<ext>), with their tests/, .solutions/ and .clarify/ beside them.
    The syllabus order is the module, then the file name (the NN numbering within the module).
    """
    found = {}
    for track_name, track in load_tracks(active_only).items():
        ext = track["extension"]
        paths = [p for p in track["dir"].rglob(f"*{ext}") if len(p.relative_to(track["dir"]).parts) >= 2]
        for path in sorted(paths, key=lambda p: (p.relative_to(track["dir"]).parts[0], p.name)):
            if any(part.startswith(".") or part in ("tests", PRIMM_DIR)
                   for part in path.relative_to(track["dir"]).parts[:-1]):
                continue
            m = STUB_RE.match(path.name)
            if not m or m.group(2) != ext:
                continue
            slug = m.group(1)
            if slug in found:
                print(f"Warning: exercise name '{slug}' is used twice; keeping {found[slug]['stub']}")
                continue
            text = path.read_text(encoding="utf-8")
            meta = {k.lower(): v.strip() for k, v in HEADER_RE.findall(text)}
            clarify = path.parent / track["clarify_file"].format(slug=slug)
            if clarify.exists():
                # The pattern lives in the hidden clarify file so the task does not give it away.
                hidden = {k.lower(): v.strip() for k, v in HEADER_RE.findall(clarify.read_text(encoding="utf-8"))}
                meta = {**hidden, **meta}
            level = meta.get("level", "easy")
            variant_of = meta.get("variant of", "")
            # workspace/<track>/<module>/<original>/ mirrors the tracks: the learner's attempt at the
            # exercise, at its variants, and that exercise's own .history/
            module_rel = Path(path.relative_to(track["dir"]).parts[0])
            exercise_ws = WORKSPACE / track_name / module_rel / (variant_of or slug)
            found[slug] = {
                "slug": slug,
                "stub": path,
                "solution": path.parent / track["solution_file"].format(slug=slug),
                "test": path.parent / track["test_file"].format(slug=slug),
                "clarify": clarify,
                "attempt": exercise_ws / f"{slug}{ext}",
                "history": exercise_ws / HISTORY_DIR,
                "module_rel": module_rel,
                "track": track_name,
                "track_config": track,
                "module": module_rel.name,
                "level": level,
                "target": int(meta.get("target", TARGETS.get(level, 15))),
                "pattern": meta.get("pattern", ""),
                "kind": meta.get("kind", "write"),
                # A variant: a new problem with the same pattern as an exercise already met; it
                # is never new material and its attempts count for that exercise's box.
                "variant_of": variant_of,
            }
    return found


def get_exercise(slug: str) -> dict:
    exercises = discover()
    if slug not in exercises:
        close = [s for s in exercises if slug in s]
        hint = f" Did you mean: {', '.join(close[:5])}?" if close else ""
        die(f"No exercise called '{slug}'.{hint} See `python dojo.py list`.")
    return exercises[slug]


def find_venv_python() -> Path | None:
    for candidate in (ROOT / ".venv" / "bin" / "python",
                      ROOT / ".venv" / "Scripts" / "python.exe"):
        if candidate.exists():
            return candidate
    return None


def venv_python() -> str:
    found = find_venv_python()
    return str(found) if found else sys.executable


def run_exercise(ex: dict, target: str | None = None, quiet: bool = False) -> bool | None:
    """Run an exercise's tests with its track's test command.

    target None = the learner's attempt (or the stub if there is none yet),
    "solution" = the reference, "stub" = the blank stub.
    Returns None when the track has no test command (log those by hand).
    """
    command = ex["track_config"].get("test_command")
    if not command:
        return None
    if target == "solution":
        source = ex["solution"]
    elif target == "stub":
        source = ex["stub"]
    else:
        source = ex["attempt"] if ex["attempt"].exists() else ex["stub"]
    values = {"python": venv_python(), "test": str(ex["test"]), "source": str(source),
              "slug": ex["slug"], "root": str(ROOT), "track_dir": str(ex["track_config"]["dir"])}
    cmd = [part.format(**values) for part in command]
    env = dict(os.environ)
    env["DOJO_SOURCE"] = str(source)
    if target:
        env["DOJO_TARGET"] = target
    else:
        env.pop("DOJO_TARGET", None)
    result = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=quiet, text=True)
    return result.returncode == 0


def warn_if_unsaved(ex: dict) -> None:
    """Warn when the attempt is still byte-for-byte the stub: usually an unsaved editor buffer."""
    attempt, stub = ex["attempt"], ex["stub"]
    try:
        unchanged = attempt.read_bytes() == stub.read_bytes()
    except OSError:
        return
    if unchanged:
        print(f"Warning: {attempt.relative_to(ROOT).as_posix()} is unchanged from the stub. "
              "Did you save the file?", file=sys.stderr)


def debug_in_process(ex: dict, target: str | None) -> int:
    """Run a pytest-based exercise inside this process so editor breakpoints work.

    The editor's debugger must start dojo.py with the venv's Python (VS Code and Zed
    pick .venv automatically).
    """
    command = ex["track_config"].get("test_command") or []
    if not any("pytest" in part for part in command):
        die("--debug works for pytest-based tracks; debug other tracks with their own tools.")
    try:
        import pytest
    except ImportError:
        die("pytest is not importable here: start the debugger with the .venv interpreter.")
    if target:
        os.environ["DOJO_TARGET"] = target
    else:
        os.environ.pop("DOJO_TARGET", None)
    os.chdir(ROOT)
    return pytest.main(["-q", "--no-header", "-p", "no:cacheprovider", str(ex["test"])])


def side_track(path: Path) -> dict | None:
    """The track whose workspace folder holds this file (workspace/<track>/...), if any."""
    try:
        name = path.resolve().relative_to(WORKSPACE.resolve()).parts[0]
    except (ValueError, IndexError):
        return None
    return load_tracks(active_only=False).get(name)


def test_slug(track: dict, path: Path) -> str | None:
    """The slug a test file belongs to, from the track's test_file pattern; None if not a test."""
    pattern = Path(track["test_file"]).name
    regex = "^" + re.escape(pattern).replace(re.escape("{slug}"), "(.+)") + "$"
    m = re.match(regex, path.name)
    return m.group(1) if m else None


def exercise_hash(ex: dict) -> str:
    """What the learner sees and is tested on: task, tests and clarify answers."""
    h = hashlib.sha256()
    for path in (ex["stub"], ex["test"], ex["clarify"]):
        h.update(path.read_bytes() if path.exists() else b"")
    return h.hexdigest()[:16]


TOPICS_RE = re.compile(r"can cover:\s*(.+?)\.?\s*$", re.MULTILINE)


def module_topics() -> dict:
    """track/module -> the lesson topics its primm/README.md lists."""
    out = {}
    for track_name, track in load_tracks(active_only=True).items():
        for readme in sorted(track["dir"].glob(f"*/{PRIMM_DIR}/README.md")):
            m = TOPICS_RE.search(readme.read_text(encoding="utf-8"))
            if m:
                out[f"{track_name}/{readme.parent.parent.name}"] = [t.strip() for t in m.group(1).split(", ") if t.strip()]
    return out


def skipped_module(module: str, profile: dict) -> bool:
    return any(module.split("/")[-1].startswith(x) for x in profile.get("skip_modules", []))


def started_modules() -> set[str]:
    """Modules with at least one attempted exercise: the only ones whose changes need a question.
    New material in a module the learner has not reached yet simply waits for them there."""
    reviews = read_json(REVIEWS, {})
    return {ex["module"] for slug, ex in discover().items() if slug in reviews}


def modules_by_name() -> dict:
    """Map module folder name -> (track name, module path relative to the track, track settings)."""
    found = {}
    for ex in discover().values():
        found.setdefault(ex["module"], (ex["track"], ex["module_rel"], ex["track_config"]))
    # Read-and-discuss modules have lessons but no exercises yet: found by their primm/ folder.
    for name, track in load_tracks(active_only=True).items():
        for primm in sorted(track["dir"].glob("m[0-9][0-9]_*/primm")):
            module = primm.parent.name
            found.setdefault(module, (name, module, track))
    return found
