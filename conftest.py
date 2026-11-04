"""Route exercise imports to the right file.

Tests do `from parse_pairs import parse_pairs`. This finder decides which file
answers that import:

- default: your attempt in workspace/python/<module>/<slug>.py (the folders mirror
  tracks/python/), or the blank stub if there is none
- DOJO_TARGET=solution: the reference in <module>/.solutions/<slug>.py (tutor and verify only)
- DOJO_TARGET=stub: the blank stub (verify only)
"""

import importlib.util
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STUB_RE = re.compile(r"^[a-z]\d\d_([a-z0-9_]+)\.py$")


def _index():
    stubs = {}
    for path in (ROOT / "tracks").rglob("*.py"):
        if ".solutions" in path.parts or "tests" in path.parts or "primm" in path.parts:
            continue
        m = STUB_RE.match(path.name)
        if m:
            stubs[m.group(1)] = path
    return stubs


class DojoFinder:
    def __init__(self):
        self.stubs = _index()
        self.target = os.environ.get("DOJO_TARGET", "")

    def find_spec(self, name, path=None, target=None):
        stub = self.stubs.get(name)
        if stub is None:
            return None
        if self.target == "solution":
            source = stub.parent / ".solutions" / f"{name}.py"
        elif self.target == "stub":
            source = stub
        else:
            module = stub.parent.relative_to(ROOT / "tracks")  # e.g. python/m01_foundations
            attempt = ROOT / "workspace" / module / f"{name}.py"
            source = attempt if attempt.exists() else stub
        return importlib.util.spec_from_file_location(name, source)


sys.meta_path.insert(0, DojoFinder())
