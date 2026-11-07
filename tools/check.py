"""Checks run before a push (.githooks/pre-push) and on every pull request (.github/workflows).

    python tools/check.py [--base <git ref>]

Looks only at what changed since the base (default: origin/main), so it stays fast:
  1. no personal data tracked (progress/, workspace/, exports/, progress_archive_*)
  2. no secrets in added lines (keys, tokens, private keys)
  3. no learner name from the local profile in shared files (local runs only)
  4. changed Python files compile, changed JSON files parse
  5. changed exercises still verify: the stub fails, the reference passes
Exit code 0 = all good. Skip once in an emergency with: git push --no-verify
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PERSONAL = re.compile(r"^(progress|workspace|exports|progress_archive_[^/]*)/")
SECRETS = {
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "AWS key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}\b"),
    "API key": re.compile(r"\b(sk-[A-Za-z0-9_-]{32,}|sk-ant-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{35})\b"),
    "Google OAuth secret": re.compile(r"\bGOCSPX-[A-Za-z0-9_-]{20,}\b"),
}
SKIP_SCAN = ("tools/check.py",)  # holds the patterns themselves


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main")
    base = parser.parse_args().base
    if not git("rev-parse", "--verify", "--quiet", base).strip():
        base = git("rev-list", "--max-parents=0", "HEAD").split()[0]  # first push: check everything
    changed = [f for f in git("diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD").split()]
    problems: list[str] = []

    problems += [f"personal file is tracked: {f}" for f in git("ls-files").split() if PERSONAL.match(f)]

    added = git("diff", "-U0", f"{base}...HEAD")
    current = ""
    names = []
    profile = ROOT / "progress" / "profile.json"
    if profile.exists():  # a learner's own clone: keep their name out of shared files
        learner = json.loads(profile.read_text(encoding="utf-8")).get("learner", "").strip()
        if len(learner) >= 3:
            names.append(learner)
    for line in added.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else ""
            continue
        if not line.startswith("+") or current in SKIP_SCAN:
            continue
        for label, pattern in SECRETS.items():
            if pattern.search(line):
                problems.append(f"possible {label} in {current}")
        for name in names:
            if re.search(rf"\b{re.escape(name)}\b", line, re.IGNORECASE) and not current.startswith(".claude-plugin/"):
                problems.append(f"your name '{name}' in {current}: shared files stay personal-free")

    for f in changed:
        path = ROOT / f
        if not path.exists():
            continue
        if f.endswith(".py"):
            result = subprocess.run([sys.executable, "-m", "py_compile", str(path)], capture_output=True, text=True)
            if result.returncode:
                problems.append(f"does not compile: {f}")
        elif f.endswith(".json"):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except ValueError as e:
                problems.append(f"invalid JSON in {f}: {e}")

    slugs = sorted({m.group(1) for f in changed
                    if (m := re.search(r"(?:^|/)(?:[ebr]\d\d_|test_|\.solutions/|\.clarify/)([a-z0-9_]+)\.\w+$", f))
                    and f.startswith("tracks/")})
    if slugs:
        result = subprocess.run([sys.executable, str(ROOT / "dojo.py"), "verify", *slugs],
                                capture_output=True, text=True, cwd=ROOT)
        if result.returncode:
            problems.append("exercises do not verify:\n" + result.stdout.strip())

    if problems:
        print("Checks failed:")
        print("\n".join("  - " + p for p in dict.fromkeys(problems)))
        return 1
    print(f"Checks passed ({len(changed)} changed file(s), {len(slugs)} exercise(s) verified).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
