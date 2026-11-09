"""Checks run before a push (.githooks/pre-push) and on every pull request (.github/workflows).

    python tools/check.py [--base <git ref>]

Looks only at what changed since the base (default: origin/main), so it stays fast:
  1. no personal data tracked (progress/, workspace/, exports/, progress_archive_*)
  2. no secrets in added lines (keys, tokens, private keys)
  3. no learner name from the local profile in shared files (local runs only)
  4. changed Python files compile, changed JSON files parse
  5. changed exercises still verify: the stub fails, the reference passes
  6. each subagent says the same in .claude/agents, .codex/agents and .gemini/agents
  7. the concept graph of every changed track is valid (ids, requires, no cycles, links to
     modules, lessons and exercises): a renamed exercise or lesson topic must update graph.json
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


READ_ONLY = "You are read-only: never create, edit or delete files."


def agent_parity() -> list[str]:
    """The three copies of every subagent must agree (name, description, instructions).
    Codex and Gemini name tools differently, so a read-only Claude agent (no Write or Edit tool)
    carries READ_ONLY as the first line of its instructions in the other two."""
    try:
        import tomllib  # Python 3.11+; on 3.10 the Codex copies are not compared
    except ModuleNotFoundError:
        tomllib = None
    problems = []
    claude = {p.stem: p for p in (ROOT / ".claude" / "agents").glob("*.md")}
    for folder, ext in ((".codex/agents", ".toml"), (".gemini/agents", ".md")):
        others = {p.stem for p in (ROOT / folder).glob(f"*{ext}")}
        for name in sorted(set(claude) ^ others):
            problems.append(f"subagent '{name}' is in only one of .claude/agents and {folder}")
    for name, path in claude.items():
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", path.read_text(encoding="utf-8"), re.DOTALL)
        meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.MULTILINE))
        body = m.group(2).strip()
        tools = {t.strip() for t in meta.get("tools", "").split(",") if t.strip()}
        if tools and not tools & {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
            body = f"{READ_ONLY}\n\n{body}"
        codex = ROOT / ".codex" / "agents" / f"{name}.toml"
        if codex.exists() and tomllib:
            t = tomllib.loads(codex.read_text(encoding="utf-8"))
            if (t.get("name"), t.get("description"), t.get("developer_instructions", "").strip()) != \
                    (meta["name"], meta["description"], body):
                problems.append(f".codex/agents/{name}.toml differs from .claude/agents/{name}.md")
        gemini = ROOT / ".gemini" / "agents" / f"{name}.md"
        if gemini.exists():
            g = re.match(r"^---\n(.*?)\n---\n(.*)$", gemini.read_text(encoding="utf-8"), re.DOTALL)
            gmeta = dict(re.findall(r"^(\w+):\s*(.*)$", g.group(1), re.MULTILINE)) if g else {}
            gdesc = json.loads(gmeta["description"]) if gmeta.get("description", "").startswith('"') \
                else gmeta.get("description")
            if not g or (gmeta.get("name"), gdesc, g.group(2).strip()) != (meta["name"], meta["description"], body):
                problems.append(f".gemini/agents/{name}.md differs from .claude/agents/{name}.md")
    return problems


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

    problems += [p + " (edit all three copies of an agent together)" for p in agent_parity()]

    graph_code_changed = any(f.startswith("dojolib/graph") for f in changed)
    tracks = sorted({f.split("/")[1] for f in changed if f.startswith("tracks/") and f.count("/") >= 2}
                    if not graph_code_changed else
                    {p.parent.name for p in (ROOT / "tracks").glob("*/graph.json")})
    tracks = [t for t in tracks if (ROOT / "tracks" / t / "graph.json").exists()]
    if tracks:
        result = subprocess.run([sys.executable, str(ROOT / "dojo.py"), "graph", "check", "--quiet", *tracks],
                                capture_output=True, text=True, cwd=ROOT)
        if result.returncode:
            problems.append("concept graph errors:\n" + result.stdout.strip())

    if problems:
        print("Checks failed:")
        print("\n".join("  - " + p for p in dict.fromkeys(problems)))
        return 1
    print(f"Checks passed ({len(changed)} changed file(s), {len(slugs)} exercise(s) verified).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
