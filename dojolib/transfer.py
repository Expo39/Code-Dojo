"""Moving personal data between machines: export, import and the Google Drive set-up."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from .core import (
    LOG, PROFILE, PROGRESS, ROOT, STAMP_FMT, WORKSPACE, die, load_profile, now, read_json,
    write_json
)
from .migrate import migrate_dates, migrate_workspace
from .graph import graph_refresh, graph_track_names, load_graph, write_graph_views


def cmd_export(args) -> None:
    """Zip all personal data (progress/ and workspace/, including the concept-graph evidence and
    probe reports), plus a fresh view of each concept graph in views/; optionally copy it away."""
    import zipfile
    profile = load_profile(required=False)
    target = args.to or profile.get("export_target")
    if target and (target.startswith("-") or target.startswith("rclone:-")):
        die(f"Refusing export target '{target}': a target cannot start with '-' "
            "(it would be read as an option).")
    name = re.sub(r"[^A-Za-z0-9_-]", "", profile.get("learner") or "learner") or "learner"
    out_dir = Path(args.out).expanduser() if args.out else ROOT / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"code-dojo_{name}_{now().strftime(STAMP_FMT)}.zip"
    count = 0
    views = []
    for track in graph_track_names(profile):
        graph = load_graph(track)
        _, states = graph_refresh(graph)  # the evidence in the backup is current
        views += write_graph_views(graph, states, out_dir / f".views_{archive.stem}")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for view in views:
            # Readable without the dojo (open the .html in a browser); never restored by import.
            z.write(view, f"views/{view.name}")
            view.unlink()
        if views:
            views[0].parent.rmdir()
        for folder in (PROGRESS, WORKSPACE):
            if not folder.exists():
                continue
            for path in folder.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts:
                    z.write(path, path.relative_to(ROOT).as_posix())
                    count += 1
    print(f"Exported {count} files to {archive}" + (f" (and {len(views)} concept-graph views in views/)" if views else ""))
    if target and target.startswith("rclone:"):
        remote = target[len("rclone:"):]
        print(f"Uploading to {remote} with rclone ...")
        if run_rclone(["copy", str(archive), remote], mounts={archive.parent: "/data"},
                      local_args={str(archive): f"/data/{archive.name}"}) != 0:
            die("rclone upload failed; the zip is still on this machine. "
                "Run `python dojo.py drive-setup` if the remote is not configured yet.")
        print("Uploaded. On the other device, download the zip, then: python dojo.py import <zip>")
    elif target:
        if shutil.which("scp") is None:
            die("scp not found. Install OpenSSH (built into Windows 10+, macOS and most Linux) "
                "or copy the zip by hand.")
        print(f"Copying to {target} ...")
        result = subprocess.run(["scp", "--", str(archive), target])
        if result.returncode != 0:
            die("scp failed; the zip is still on this machine.")
        print("Copied. On the other device: python dojo.py import <zip>")


RCLONE_IMAGE = "rclone/rclone:1.71"


def run_rclone(rclone_args: list, mounts: dict | None = None, local_args: dict | None = None,
               interactive: bool = False) -> int:
    """Run rclone from PATH, or else from its Docker image (config in ~/.config/rclone)."""
    sys.stdout.flush()
    if shutil.which("rclone"):
        return subprocess.run(["rclone", *rclone_args]).returncode
    if shutil.which("docker") is None:
        die("rclone not found. Install Docker (the rclone image is then pulled automatically) "
            "or rclone itself (https://rclone.org/install/).")
    config = Path.home() / ".config" / "rclone"
    config.mkdir(parents=True, exist_ok=True)
    cmd = ["docker", "run", "--rm", "-v", f"{config}:/config/rclone"]
    if interactive:
        cmd += ["--network", "host"]  # the Google sign-in calls back to localhost
        cmd += ["-it"] if sys.stdin.isatty() else ["-i"]
    if hasattr(os, "getuid"):
        cmd += ["--user", f"{os.getuid()}:{os.getgid()}"]
    for host_dir, container_dir in (mounts or {}).items():
        cmd += ["-v", f"{host_dir}:{container_dir}:ro"]
    args = [(local_args or {}).get(a, a) for a in rclone_args]
    return subprocess.run([*cmd, RCLONE_IMAGE, *args]).returncode


def cmd_drive_setup(args) -> None:
    """One-time Google Drive sign-in for rclone, then save the export target."""
    remote = args.remote
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", remote) or remote.startswith("-") or args.folder.startswith("-"):
        die("Remote and folder names: letters, digits, '_', '.', '-', not starting with '-'.")
    print(f"Creating the rclone remote '{remote}' for Google Drive. A sign-in link opens or is "
          "printed: log in with the Google account that should hold the exports.")
    if run_rclone(["config", "create", remote, "drive", "scope=drive.file"], interactive=True) != 0:
        die("rclone config failed.")
    target = f"rclone:{remote}:{args.folder}"
    profile = read_json(PROFILE, None)
    if profile is not None:
        profile["export_target"] = target
        write_json(PROFILE, profile)
        print(f"Saved export_target = {target}. From now on `python dojo.py export` uploads there.")
    else:
        print(f"Done. Export with: python dojo.py export --to {target}")


def cmd_import(args) -> None:
    """Restore progress/ and workspace/ from an export zip."""
    import zipfile
    archive = Path(args.archive).expanduser()
    if not archive.exists():
        die(f"No such file: {archive}")
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        restore = [n for n in names if not n.startswith("views/")]  # views/ is regenerated, not data
        bad = [n for n in names if not (n.startswith(("progress/", "workspace/", "views/")))
               or ".." in n.replace("\\", "/").split("/") or "\\" in n or ":" in n]
        links = [i.filename for i in z.infolist() if (i.external_attr >> 16) & 0o170000 == 0o120000]
        if links:
            die(f"Refusing: the zip contains a symbolic link ({links[0]}).")
        if bad:
            die(f"Refusing: unexpected paths in the zip, e.g. {bad[0]}")
        has_data = PROFILE.exists() or LOG.exists()
        if has_data and not args.force:
            die("This copy already has progress. Run `python dojo.py export` first to keep it, "
                "then `python dojo.py import <zip> --force`.")
        if has_data:
            stamp = now().strftime(STAMP_FMT)
            backup = ROOT / f"progress_archive_{stamp}"
            backup.mkdir()
            for folder in (PROGRESS, WORKSPACE):
                if folder.exists():
                    shutil.move(str(folder), backup / folder.name)
            print(f"Current data moved to {backup.name}/")
        z.extractall(ROOT, members=restore)
    migrate_workspace(verbose=False)  # an export from an older version may use the flat layout
    migrate_dates(verbose=False)
    print(f"Imported {len(restore)} files. Run `python dojo.py today`.")
