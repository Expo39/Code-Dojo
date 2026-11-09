"""One-off migrations of older layouts: the progress/ layout, per-module workspace folders, drill
and mock type folders, and European dates."""

from __future__ import annotations

import csv
import re
import shutil
from datetime import date

from .core import (
    FILE_DATE_FMT, HISTORY_DIR, LAYOUT, LOG, LOG_FIELDS, MISTAKES, PERSONAL_DOCS, PROFILE, PROGRESS,
    REVIEWS, ROOT, SESSION, TRACK_REPORT_DIRS, TRACKER, UPSTREAM_CHECK, WEEKLY, WORKSPACE,
    active_track_names, fmt_date, parse_date, read_json, track_progress, write_json
)
from .data import ensure_files, read_log
from .tracks import discover, load_tracks, test_slug


TRACK_SIDE_FOLDERS = ("drills", "mocks")  # workspace/<track>/drills/, workspace/<track>/mocks/
# Drills and mocks live in type folders: drills/<type>/<focus>.<ext>,
# mocks/<type>/<problem>_<DD_MM_YYYY>.<ext>. Older flat files named <type>_... are moved into
# the folder of their prefix; these are the drill types such files can carry.
DRILL_TYPES = ("bug", "predict", "trace", "review", "explain")
LEGACY_MOCKS = "earlier"  # flat mock_<date> files from before the type folders
HISTORY_STAMP_RE = re.compile(r"^(?P<slug>[a-z0-9_]+?)_\d{8}_\d{4}(?P<ext>\.[A-Za-z0-9]+)$")


def migrate_workspace(verbose: bool = True) -> int:
    """Move files from the old flat layout into workspace/<track>/<module>/. Idempotent.

    Old layout: workspace/<track>/<slug>.<ext>, workspace/.history/<slug>_<stamp>.<ext>, and
    workspace/drills/ and workspace/mocks/ (now workspace/<track>/drills/ and .../mocks/).
    Loose files that are not exercises go to workspace/<track>/scratch/. Nothing is
    overwritten: a name clash is reported and left in place.
    """
    if not WORKSPACE.exists():
        return 0
    exercises = discover(active_only=False)
    moves = []
    for track_name in load_tracks(active_only=False):
        folder = WORKSPACE / track_name
        if not folder.is_dir():
            continue
        for path in sorted(p for p in folder.iterdir() if p.is_file()):
            ex = exercises.get(path.stem)
            if ex and ex["track"] == track_name and path.suffix == ex["attempt"].suffix:
                moves.append((path, ex["attempt"]))
            elif path.name != ".gitkeep":
                moves.append((path, folder / "scratch" / path.name))
        cache = folder / "__pycache__"
        if cache.is_dir():
            shutil.rmtree(cache)
    # drills/ and mocks/ used to sit at the workspace root; they belong to the track whose
    # extension the file has (left in place when no single active track matches)
    active = load_tracks(active_only=True)
    for kind in TRACK_SIDE_FOLDERS:
        old = WORKSPACE / kind
        if not old.is_dir():
            continue
        for path in sorted(p for p in old.iterdir() if p.is_file()):
            owners = [t for t, s in active.items() if s["extension"] == path.suffix]
            if len(owners) == 1:
                moves.append((path, WORKSPACE / owners[0] / kind / path.name))
            else:
                print(f"  migrate: kept {path.relative_to(ROOT).as_posix()} "
                      f"(no single active track uses {path.suffix or 'no extension'})")
        cache = old / "__pycache__"
        if cache.is_dir():
            shutil.rmtree(cache)
    old_history = WORKSPACE / HISTORY_DIR
    if old_history.is_dir():
        for path in sorted(p for p in old_history.iterdir() if p.is_file()):
            m = HISTORY_STAMP_RE.match(path.name)
            ex = exercises.get(m.group("slug")) if m else None
            if ex:
                moves.append((path, ex["attempt"].parent / HISTORY_DIR / path.name))
    moved = 0
    for src, dest in moves:
        if dest.exists():
            print(f"  migrate: kept {src.relative_to(ROOT).as_posix()} "
                  f"({dest.relative_to(ROOT).as_posix()} already exists)")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), dest)
        moved += 1
        if verbose:
            print(f"  moved {src.relative_to(ROOT).as_posix()} -> {dest.relative_to(ROOT).as_posix()}")
    for old in [old_history] + [WORKSPACE / kind for kind in TRACK_SIDE_FOLDERS]:
        if old.is_dir() and not any(old.iterdir()):
            old.rmdir()
    # generated folders (drills/, mocks/) hold only the files the learner works in; their tests
    # sit in a tests/ subfolder, and import from the folder above
    for track_name, track in load_tracks(active_only=False).items():
        for kind in TRACK_SIDE_FOLDERS:
            folder = WORKSPACE / track_name / kind
            if not folder.is_dir():
                continue
            for path in sorted(p for p in folder.iterdir() if p.is_file() and test_slug(track, p)):
                dest = folder / track["test_file"].format(slug=test_slug(track, path))
                if dest.parent == folder or dest.exists():
                    continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                text = path.read_text(encoding="utf-8")
                dest.write_text(text.replace("Path(__file__).parent)", "Path(__file__).parent.parent)"),
                                encoding="utf-8")
                path.unlink()
                moved += 1
                if verbose:
                    print(f"  moved {path.relative_to(ROOT).as_posix()} -> "
                          f"{dest.relative_to(ROOT).as_posix()}")
            cache = folder / "__pycache__"
            if cache.is_dir():
                shutil.rmtree(cache)
    moved += migrate_side_folders(verbose)
    if moved:
        print(f"Workspace reorganised by module: {moved} file(s) moved.")
    return moved


def migrate_side_folders(verbose: bool = True) -> int:
    """Move flat drills/ and mocks/ files into type folders. Idempotent.

    Old layout: drills/bug_<n>.<ext>, mocks/mock_<date>.<ext>, each with its test file (the
    track's test_file pattern, e.g. tests/test_<stem>.py) and .history/<stem>_original. A drill goes to drills/<type>/ (the type is its name's
    prefix, else "other"); a mock goes to mocks/earlier/, as its type was never recorded.
    The stem is kept, so the tests still import it; the tutor may rename them later.
    """
    moved = 0
    for track_name, track in load_tracks(active_only=False).items():
        for kind in TRACK_SIDE_FOLDERS:
            folder = WORKSPACE / track_name / kind
            if not folder.is_dir():
                continue
            for path in sorted(p for p in folder.iterdir() if p.is_file() and p.name != ".gitkeep"):
                if kind == "drills":
                    prefix = path.stem.split("_")[0]
                    group = prefix if prefix in DRILL_TYPES else "other"
                else:
                    group = LEGACY_MOCKS
                dest_dir = folder / group
                if test_slug(track, path):
                    continue  # a test file left beside the drills; the tests/ step moves those
                test_rel = track["test_file"].format(slug=path.stem)
                pairs = [(path, dest_dir / path.name), (folder / test_rel, dest_dir / test_rel),
                         (folder / HISTORY_DIR / f"{path.stem}_original{path.suffix}",
                          dest_dir / HISTORY_DIR / f"{path.stem}_original{path.suffix}")]
                for src, dest in pairs:
                    if not src.is_file():
                        continue
                    if dest.exists():
                        print(f"  migrate: kept {src.relative_to(ROOT).as_posix()} "
                              f"({dest.relative_to(ROOT).as_posix()} already exists)")
                        continue
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), dest)
                    moved += 1
                    if verbose:
                        print(f"  moved {src.relative_to(ROOT).as_posix()} -> "
                              f"{dest.relative_to(ROOT).as_posix()}")
            for sub in (folder / "tests", folder / HISTORY_DIR):
                cache = sub / "__pycache__"
                if cache.is_dir():
                    shutil.rmtree(cache)
                if sub.is_dir() and not any(sub.iterdir()):
                    sub.rmdir()
            cache = folder / "__pycache__"
            if cache.is_dir():
                shutil.rmtree(cache)
    return moved


OLD_TRACKER_FILES = ("timer.json", "session.json", "tracks_seen.json", "topics_seen.json",
                     "upstream_check.json")  # at the top of progress/ before progress/tracker/
PROGRESS_LAYOUT = 2  # 2 = shared notes at the top, one folder per track, tracker/ for bookkeeping


def migrate_progress(verbose: bool = True) -> int:
    """Move an older flat progress/ into the current layout (docs/PERSONAL_DOCS.md). Idempotent.

    The tracker's bookkeeping goes to progress/tracker/; drill, mock and probe reports, the
    revisits list and the old notes go to the first track's folder (everything before this
    layout was written for one track); fresh shared notes are created by ensure_files. The
    tutor then moves what holds in any language back to the shared notes (dojo-weekly)."""
    if not PROGRESS.is_dir() or read_json(LAYOUT, {}).get("progress") == PROGRESS_LAYOUT:
        return 0
    moved = []
    TRACKER.mkdir(exist_ok=True)
    for name in OLD_TRACKER_FILES:
        if (PROGRESS / name).exists() and not (TRACKER / name).exists():
            moved.append((PROGRESS / name, TRACKER / name))
    old_habits = PROGRESS / "WORK_HABITS.md"  # older checkouts kept it at the top of progress/
    if old_habits.exists() and not (PERSONAL_DOCS / "WORK_HABITS.md").exists():
        moved.append((old_habits, PERSONAL_DOCS / "WORK_HABITS.md"))
    tracks = active_track_names()
    if tracks:
        home = track_progress(tracks[0])
        for kind in TRACK_REPORT_DIRS:
            if (PROGRESS / kind).is_dir():
                moved += [(f, home / kind / f.name) for f in sorted((PROGRESS / kind).iterdir())]
        old_layout = not (home / "mistakes.md").exists()
        for name in ("revisits.md", *(("mistakes.md", "cheatsheet.md", "approaches.md") if old_layout else ())):
            if (PROGRESS / name).exists() and not (home / name).exists():
                moved.append((PROGRESS / name, home / name))
    for src, dest in moved:
        if dest.exists():
            print(f"  layout: kept {src.relative_to(ROOT).as_posix()} ({dest.relative_to(ROOT).as_posix()} already exists)")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), dest)
        if verbose:
            print(f"  moved {src.relative_to(ROOT).as_posix()} -> {dest.relative_to(ROOT).as_posix()}")
    for kind in TRACK_REPORT_DIRS:
        if (PROGRESS / kind).is_dir() and not any((PROGRESS / kind).iterdir()):
            (PROGRESS / kind).rmdir()
    write_json(LAYOUT, {"progress": PROGRESS_LAYOUT})
    ensure_files()  # the shared notes and every track's folder
    if moved and verbose:
        print(f"progress/ reorganised: {len(moved)} file(s) moved (shared notes at the top, "
              "one folder per track, tracker/ for bookkeeping).")
    return len(moved)


ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
ISO_IN_NAME_RE = re.compile(r"(?<!\d)(20\d{2})[-_](0[1-9]|1[0-2])[-_](0[1-9]|[12]\d|3[01])(?!\d)")
ISO_STAMP_RE = re.compile(r"(?<!\d)(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])_(\d{4,6})(?!\d)")


def is_dated_row(line: str) -> bool:
    """A markdown table row whose first cell is a date (the mistakes log)."""
    cells = line.split("|")
    if len(cells) < 3 or not line.startswith("|"):
        return False
    try:
        parse_date(cells[1])
        return True
    except ValueError:
        return False


def euro_date(text: str) -> str:
    """An ISO date string as DD/MM/YYYY; anything else unchanged."""
    return fmt_date(date.fromisoformat(text)) if text and ISO_DATE_RE.match(text) else text


def euro_name(name: str, sep: str = "_") -> str:
    """ISO dates and stamps inside a file or item name, turned day-first."""
    name = ISO_STAMP_RE.sub(lambda m: f"{m[3]}{m[2]}{m[1]}_{m[4]}", name)
    return ISO_IN_NAME_RE.sub(lambda m: f"{m[3]}{sep}{m[2]}{sep}{m[1]}", name)


def migrate_dates(verbose: bool = True) -> int:
    """Turn ISO dates in personal data and file names into the European format. Idempotent."""
    changes = 0
    if LOG.exists():
        rows = read_log()
        new = [dict(r, date=euro_date(r["date"]), item=euro_name(r["item"])) for r in rows]
        if new != rows:
            with LOG.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
                writer.writeheader()
                writer.writerows({k: r.get(k, "") for k in LOG_FIELDS} for r in new)
            changes += 1
    reviews = read_json(REVIEWS, None)
    if reviews:
        new = {k: dict(c, **{f: euro_date(c[f]) for f in ("last", "due") if c.get(f)})
               for k, c in reviews.items()}
        if new != reviews:
            write_json(REVIEWS, new)
            changes += 1
    for path, keys in ((PROFILE, ("start_date", "target_date")), (UPSTREAM_CHECK, ("date",)),
                       (SESSION, ("date",))):
        data = read_json(path, None)
        if isinstance(data, dict):
            new = dict(data, **{k: euro_date(data[k]) for k in keys if isinstance(data.get(k), str)})
            if new != data:
                write_json(path, new)
                changes += 1
    for log in [MISTAKES, *PROGRESS.glob("*/mistakes.md")]:
        if log.exists():
            text = log.read_text(encoding="utf-8")
            new = re.sub(r"^\| (\d{4}-\d{2}-\d{2}) \|", lambda m: f"| {euro_date(m[1])} |", text, flags=re.M)
            if new != text:
                log.write_text(new, encoding="utf-8")
                changes += 1
    renames = []
    for mocks in PROGRESS.glob("*/mocks"):
        renames += [(p, p.with_name(euro_name(p.name, "-"))) for p in mocks.iterdir()]
    if WEEKLY.is_dir():
        for p in WEEKLY.glob("*-W*.md"):
            m = re.fullmatch(r"(\d{4})-W(\d{2})\.md", p.name)
            if m:
                monday = date.fromisocalendar(int(m[1]), int(m[2]), 1)
                renames.append((p, WEEKLY / f"week_{monday.strftime(FILE_DATE_FMT)}.md"))
    for folder in (WORKSPACE, ROOT / "exports"):
        if folder.is_dir():
            renames += [(p, p.with_name(euro_name(p.name))) for p in folder.rglob("*")
                        if p.is_file() and "__pycache__" not in p.parts]
    for src, dest in renames:
        if src == dest:
            continue
        if dest.exists():
            print(f"  dates: kept {src.relative_to(ROOT).as_posix()} ({dest.name} already exists)")
            continue
        if src.suffix in (".py", ".md", ".txt"):  # a test imports its module by name
            text = src.read_text(encoding="utf-8")
            new = euro_name(text)
            if new != text:
                src.write_text(new, encoding="utf-8")
        src.rename(dest)
        changes += 1
        if verbose:
            print(f"  renamed {src.relative_to(ROOT).as_posix()} -> {dest.name}")
    if changes and verbose:
        print(f"Dates switched to DD/MM/YYYY: {changes} file(s) updated.")
    return changes


def cmd_migrate(args) -> None:
    if not migrate_progress(verbose=True):
        print("progress/ already in the current layout.")
    if not migrate_workspace(verbose=True):
        print("Workspace already in the per-module layout.")
    if not migrate_dates(verbose=True):
        print("Dates already in the European format.")
