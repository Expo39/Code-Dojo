"""The concept graph: each track's tracks/<track>/graph.json (concepts, what each needs first,
the observable "can" statement, the lesson and the exercises) and the learner's evidence in
progress/graph.json. A concept's state is computed from that evidence and the live redo boxes,
never stored twice (docs/TRACKS.md, "Concept graph")."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

from .core import (
    GRAPH_OVERLAY, PRIMM_DIR, REVIEWS, ROOT, active_track_names, die, fmt_date, load_profile,
    parse_date, read_json, today, write_json
)
from .data import ensure_files, read_log
from .tracks import TOPICS_RE, discover, load_tracks
from .planning import recent_stats


GRAPH_FILE = "graph.json"
GRAPH_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
EVIDENCE_STATES = ("gap", "misconception", "fragile", "held")
EVIDENCE_SOURCES = ("probe", "lesson", "tutor", "exercise", "mock", "drill", "import", "placement")
SOLID = ("fluent", "held", "due")  # good enough to build on
STATE_STYLE = {  # display order, label, ANSI colour
    "fluent": ("fluent", "32"), "held": ("held", "36"), "due": ("due", "33"),
    "fragile": ("fragile", "33"), "misconception": ("misconc.", "31"), "gap": ("gap", "31"),
    "ready": ("ready", "35"), "unknown": ("-", "2"), "planned": ("planned", "2"),
}
SHARED_STORE = "_shared"  # overlay key for concepts marked "shared": the same in every language
_GRAPHS: dict = {}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")


def build_graph(name: str, concepts: dict[str, dict], parts: list[dict], **extra) -> dict:
    """Adjacency, order and lookups for a set of concepts (one track's, or every track's)."""
    dependents: dict[str, list[str]] = {cid: [] for cid in concepts}
    for c in concepts.values():
        for r in c["requires"]:
            if r in dependents:
                dependents[r].append(c["id"])
    order, cycle = topo_order(concepts)
    by_exercise: dict[str, list[str]] = {}
    by_lesson: dict[str, list[str]] = {}
    for c in concepts.values():
        for slug in c["exercises"]:
            by_exercise.setdefault(slug, []).append(c["id"])
        for lesson in [c["lesson"], *c["aliases"]]:
            if lesson:
                by_lesson.setdefault(slugify(lesson), []).append(c["id"])
    graph = {"track": name, "concepts": concepts, "dependents": dependents, "order": order,
             "cycle": cycle, "rank": {cid: i for i, cid in enumerate(order)},
             "by_exercise": by_exercise, "by_lesson": by_lesson, **extra}
    graph["parts"] = parts or [graph]
    return graph


def load_graph(track: str) -> dict | None:
    """The track's concept graph with adjacency built once (cached on the file's mtime)."""
    config = load_tracks(active_only=False).get(track)
    if not config:
        return None
    path = config["dir"] / GRAPH_FILE
    if not path.exists():
        return None
    key = (str(path), path.stat().st_mtime_ns)
    if key in _GRAPHS:
        return _GRAPHS[key]
    data = read_json(path, {})
    raw = data.get("concepts", [])
    concepts: dict[str, dict] = {}
    for c in raw:
        c = {"requires": [], "exercises": [], "aliases": [], "lesson": "", "kind": "skill",
             "planned": False, "shared": False, "can": "", **c}
        c["name"] = c.get("name") or c["id"]
        # Where its evidence lives: a shared concept is the same in every track (SHARED_STORE).
        c.update(track=track, local=c["id"], store=SHARED_STORE if c["shared"] else track)
        concepts.setdefault(c["id"], c)
    graph = build_graph(track, concepts, [], slug=track, path=path, data=data, raw=raw, config=config)
    _GRAPHS[key] = graph
    return graph


def combined_graph(names: list[str]) -> dict:
    """Every track's graph as one: a shared concept appears once (its prerequisites and
    exercises from every track joined); a concept id used by two tracks becomes <track>:<id>."""
    parts = [g for g in (load_graph(t) for t in names) if g]
    if len(parts) == 1:
        return parts[0]
    owners: dict[str, set[str]] = {}
    for part in parts:
        for c in part["concepts"].values():
            owners.setdefault(c["local"], set()).add(SHARED_STORE if c["shared"] else part["track"])
    def key(c: dict) -> str:
        return c["local"] if c["shared"] or len(owners[c["local"]]) == 1 else f"{c['track']}:{c['local']}"
    concepts: dict[str, dict] = {}
    for part in parts:
        for c in part["concepts"].values():
            k = key(c)
            reqs = [key(part["concepts"][r]) for r in c["requires"] if r in part["concepts"]]
            if k in concepts:  # the same shared concept from another track
                merged = concepts[k]
                merged["requires"] += [r for r in reqs if r not in merged["requires"]]
                merged["exercises"] += [x for x in c["exercises"] if x not in merged["exercises"]]
                merged["aliases"] += [a for a in [c["lesson"], *c["aliases"]] if a and a not in merged["aliases"]]
                merged["planned"] = merged["planned"] and c["planned"]
            else:
                concepts[k] = {**c, "id": k, "requires": reqs, "exercises": list(c["exercises"]),
                               "aliases": list(c["aliases"])}
    return build_graph("all tracks", concepts, parts, slug="all")


def topo_order(concepts: dict) -> tuple[list[str], list[str]]:
    """Kahn's algorithm in file order, O(V+E). Returns (order, a cycle if one exists)."""
    indegree = {cid: sum(1 for r in c["requires"] if r in concepts) for cid, c in concepts.items()}
    dependents: dict[str, list[str]] = {cid: [] for cid in concepts}
    for cid, c in concepts.items():
        for r in c["requires"]:
            if r in concepts:
                dependents[r].append(cid)
    ready = [cid for cid in concepts if indegree[cid] == 0]
    order: list[str] = []
    i = 0
    while i < len(ready):
        cid = ready[i]
        i += 1
        order.append(cid)
        for d in dependents[cid]:
            indegree[d] -= 1
            if indegree[d] == 0:
                ready.append(d)
    if len(order) == len(concepts):
        return order, []
    left = [cid for cid in concepts if indegree[cid] > 0]
    # Walk prerequisites inside the leftover set until a node repeats: that loop is a cycle.
    seen: dict[str, int] = {}
    path: list[str] = []
    node = left[0]
    while node not in seen:
        seen[node] = len(path)
        path.append(node)
        node = next(r for r in concepts[node]["requires"] if r in concepts and indegree[r] > 0)
    cycle = path[seen[node]:] + [node]
    return order + left, cycle


def graph_ancestors(graph: dict, ids) -> set[str]:
    """Every prerequisite of the given concepts, transitively (iterative DFS)."""
    concepts = graph["concepts"]
    seen: set[str] = set()
    stack = [r for cid in ids for r in concepts[cid]["requires"] if r in concepts]
    while stack:
        cid = stack.pop()
        if cid not in seen:
            seen.add(cid)
            stack.extend(r for r in concepts[cid]["requires"] if r in concepts and r not in seen)
    return seen


def graph_targets(graph: dict, names: list[str]) -> list[str]:
    """Resolve concept ids, module names (or prefixes such as m22) and exercise slugs."""
    concepts = graph["concepts"]
    out: list[str] = []
    for name in names:
        if name in concepts:
            found = [name]
        else:
            found = graph["by_exercise"].get(name) or [
                cid for cid, c in concepts.items() if c["module"] == name or c["module"].startswith(name + "_")
                or (len(name) >= 3 and c["module"].startswith(name))]
        if not found:
            die(f"'{name}' is not a concept, module or exercise of the {graph['track']} graph. "
                f"See `python dojo.py graph {graph['track']}`.")
        out.extend(cid for cid in found if cid not in out)
    return out


def graph_track_names() -> list[str]:
    """The learner's tracks that have a concept graph, in their order."""
    return [t for t in active_track_names() if load_graph(t)]


def pick_graph(track: str | None) -> dict:
    if track:
        graph = load_graph(track)
        if not graph:
            die(f"Track '{track}' has no {GRAPH_FILE}. Tracks with one: "
                + (", ".join(t for t in load_tracks(active_only=False) if load_graph(t)) or "none"))
        return graph
    names = graph_track_names()
    if not names:
        die(f"None of your tracks has a {GRAPH_FILE} yet (dojo-new-track writes one).")
    return combined_graph(names)


# Overlay: {"version": 1, "tracks": {track or SHARED_STORE: {concept: [evidence, ...]}},
#           "ingested": {track: {...}}}
# Evidence: {"state", "date", "source", "ref", "confidence"?, "note"?}

def read_overlay() -> dict:
    data = read_json(GRAPH_OVERLAY, {})
    data.setdefault("version", 1)
    data.setdefault("tracks", {})
    data.setdefault("ingested", {})
    return data


def evidence_of(overlay: dict, c: dict) -> list[dict]:
    """A concept's evidence list (a shared concept's is the same from every track)."""
    return overlay["tracks"].get(c["store"], {}).get(c["local"], [])


def settle_stores(graph: dict, overlay: dict) -> None:
    """Move evidence to where each concept now keeps it: a concept a track update made shared
    brings its evidence to SHARED_STORE, one no longer shared takes it back (refs stop doubles)."""
    for part in graph["parts"]:
        for c in part["concepts"].values():
            wrong = part["track"] if c["store"] == SHARED_STORE else SHARED_STORE
            stray = overlay["tracks"].get(wrong, {}).pop(c["local"], None)
            for entry in stray or []:
                add_evidence(overlay, c, entry)


def add_evidence(overlay: dict, c: dict, entry: dict) -> bool:
    """Append evidence unless the same ref is already there (re-running is always safe)."""
    entries = overlay["tracks"].setdefault(c["store"], {}).setdefault(c["local"], [])
    if entry.get("ref") and any(e.get("ref") == entry["ref"] for e in entries):
        return False
    entries.append({k: v for k, v in entry.items() if v not in (None, "")})
    return True


def log_row_ref(row: dict) -> str:
    return "log:" + ":".join(row.get(k, "") for k in ("date", "item", "kind", "minutes"))


def pattern_concepts(graph: dict) -> dict[str, list[str]]:
    """Exercise pattern (as logged for mocks and outside problems) -> the concepts it trains."""
    out: dict[str, list[str]] = {}
    exercises = discover(active_only=False)
    for slug, cids in graph["by_exercise"].items():
        ex = exercises.get(slug)
        if ex and ex["pattern"]:
            for cid in cids:
                out.setdefault(ex["pattern"], [])
                if cid not in out[ex["pattern"]]:
                    out[ex["pattern"]].append(cid)
    for cid, c in graph["concepts"].items():
        for name in (cid, c["lesson"], *c["aliases"]):
            if name:
                out.setdefault(slugify(name).replace("_", "-"), [cid])
    return out


def row_evidence(graph: dict, row: dict, patterns: dict) -> list[tuple[str, dict]]:
    """What one log row says about which concepts (deterministic rules, docs/TRACKS.md)."""
    kind, item, note = row.get("kind", ""), row.get("item", ""), row.get("note", "") or ""
    ref = log_row_ref(row)
    base = {"date": row.get("date", ""), "ref": ref}
    hints = int(row.get("hints") or 0)
    result = row.get("result", "")
    out: list[tuple[str, dict]] = []
    if kind == "exercise" and item in graph["by_exercise"]:
        weak = result in ("gave_up", "failed") or hints >= 3
        state = "fragile" if weak else "held"
        detail = f"{item}: {result or 'logged'}, {hints} hint(s)"
        out = [(cid, {**base, "state": state, "source": "exercise", "note": detail})
               for cid in graph["by_exercise"][item]]
    elif kind == "study" and not note.startswith(("credit:", "paused:")):
        cids = graph["by_lesson"].get(slugify(item), [])
        if note.startswith("probe"):
            cids = []
        out = [(cid, {**base, "state": "held", "source": "lesson", "note": f"lesson {item}"}) for cid in cids]
    elif kind in ("mock", "external") and row.get("pattern"):
        cids = patterns.get(row["pattern"], [])
        state = "held" if result in ("pass", "strong", "solved") and hints < 3 else "fragile"
        source = "mock" if kind == "mock" else "exercise"
        out = [(cid, {**base, "state": state, "source": source,
                      "note": f"{kind} {item}: {result}, {hints} hint(s)"}) for cid in cids]
    return out


def graph_derive(graph: dict, overlay: dict, verbose: bool = False) -> int:
    """Read new log rows into the overlay. Incremental: a checkpoint (row count and a hash of
    those rows) skips what was read before; if the log was rewritten, everything is read again
    and the refs stop duplicates. Returns the number of new evidence entries."""
    return sum(derive_track(part, overlay, verbose) for part in graph["parts"])


def derive_track(graph: dict, overlay: dict, verbose: bool) -> int:
    rows = read_log()
    track = graph["track"]
    mark = overlay["ingested"].get(track, {})
    start = 0
    if mark.get("rows", 0) <= len(rows):
        digest = hashlib.sha256("\n".join(log_row_ref(r) for r in rows[:mark.get("rows", 0)]).encode()).hexdigest()[:16]
        if digest == mark.get("hash"):
            start = mark["rows"]
    patterns = pattern_concepts(graph) if any(r.get("kind") in ("mock", "external") for r in rows[start:]) else {}
    added = 0
    for row in rows[start:]:
        for cid, entry in row_evidence(graph, row, patterns):
            added += add_evidence(overlay, graph["concepts"][cid], entry)
    overlay["ingested"][track] = {
        "rows": len(rows),
        "hash": hashlib.sha256("\n".join(log_row_ref(r) for r in rows).encode()).hexdigest()[:16],
    }
    if verbose:
        print(f"{track}: read {len(rows) - start} new log row(s), {added} new evidence entr"
              f"{'y' if added == 1 else 'ies'}.")
    return added


def graph_refresh(graph: dict, verbose: bool = False) -> tuple[dict, dict]:
    """Read new log rows into the evidence, save it if anything changed, and return
    (overlay, states): the one way every command gets current concept states."""
    overlay = read_overlay()
    before = json.dumps(overlay, sort_keys=True)
    settle_stores(graph, overlay)
    graph_derive(graph, overlay, verbose=verbose)
    if json.dumps(overlay, sort_keys=True) != before:
        write_json(GRAPH_OVERLAY, overlay)
    return overlay, concept_states(graph, overlay, today())


def concept_states(graph: dict, overlay: dict, on: date) -> dict[str, dict]:
    """State of every concept: the latest evidence, then the live redo boxes of its exercises."""
    reviews = read_json(REVIEWS, {})
    out: dict[str, dict] = {}
    for cid in graph["order"]:
        c = graph["concepts"][cid]
        entries = sorted(enumerate(evidence_of(overlay, c)),
                         key=lambda ie: (parse_date(ie[1]["date"]) if ie[1].get("date") else date.min, ie[0]))
        latest = entries[-1][1] if entries else None
        state = latest["state"] if latest else "unknown"
        cards = [reviews[s] for s in c["exercises"] if s in reviews]
        due = [s for s in c["exercises"] if s in reviews and parse_date(reviews[s]["due"]) <= on]
        if cards:
            last_review = max(parse_date(card["last"]) for card in cards if card.get("last"))
            newer_doubt = latest and latest["state"] in ("misconception", "gap") and latest.get("date") \
                and parse_date(latest["date"]) > last_review
            practised = [s for s in c["exercises"] if s in reviews]
            if not newer_doubt:
                if len(practised) == len(c["exercises"]) and all(card["box"] >= 2 for card in cards):
                    state = "fluent"
                elif state == "unknown":
                    state = "held" if any(card["box"] >= 1 for card in cards) else "fragile"
            if due and state in ("fluent", "held"):
                state = "due"
        if state == "unknown" and c["planned"]:
            state = "planned"
        out[cid] = {"state": state, "latest": latest, "due": due, "evidence": [e for _, e in entries]}
    # Using a concept well implies holding what it is built on: a concept with no evidence of
    # its own under a solid one counts as held (walked top-down, so it reaches every level).
    for cid in reversed(graph["order"]):
        info = out[cid]
        if info["state"] in ("unknown", "planned") and any(out[d]["state"] in SOLID for d in graph["dependents"][cid]):
            info["state"] = "held"
            info["implied"] = True
    for cid in graph["order"]:
        info = out[cid]
        if info["state"] in ("unknown", "gap", "planned"):
            reqs = [r for r in graph["concepts"][cid]["requires"] if r in out]
            if all(out[r]["state"] in SOLID for r in reqs):
                info["ready"] = True
                if info["state"] == "unknown":
                    info["state"] = "ready"
    return out


def unlocks(graph: dict, states: dict, cid: str) -> int:
    """How many concepts would become ready once this one is solid (0 if it already is)."""
    if states[cid]["state"] in SOLID:
        return 0
    n = 0
    for d in graph["dependents"][cid]:
        if states[d]["state"] in SOLID:
            continue
        reqs = [r for r in graph["concepts"][d]["requires"] if r in states and r != cid]
        if all(states[r]["state"] in SOLID for r in reqs):
            n += 1
    return n


def concept_action(graph: dict, cid: str, info: dict, done_lessons: set[str]) -> str:
    c = graph["concepts"][cid]
    reviews = read_json(REVIEWS, {})
    if c["planned"]:
        return f"planned module {c['module']}: no material yet"
    if info["due"]:
        return "redo " + ", ".join(info["due"][:3])
    lesson = c["lesson"] or (f"theory_{cid.removeprefix('theory_')}" if c["kind"] == "theory" else "")
    lesson_done = any(slugify(n) in done_lessons for n in [c["lesson"], *c["aliases"]] if n)
    fresh = [s for s in c["exercises"] if s not in reviews]
    if info["state"] in ("misconception", "gap", "fragile"):
        if lesson and not lesson_done:
            return f"repair: teach me {lesson} ({c['module']})"
        practised = [s for s in c["exercises"] if s in reviews]
        return "repair: redo " + ", ".join(practised[:2]) if practised else f"repair: discuss it ({c['can']})"
    if lesson and not lesson_done:
        return f"teach me {lesson} ({c['module']})"
    if fresh:
        return f"start {fresh[0]}"
    return "drill it or redo its exercises"


def graph_next(graph: dict, states: dict, goal: list[str] | None = None, limit: int = 8) -> list[tuple[str, str]]:
    """Ranked list of what can be done now: (concept, action)."""
    tree = (graph_ancestors(graph, goal) | set(goal)) if goal else set()
    weak_patterns = {p for p, s in recent_stats(read_log(), 14, today()).items()
                     if s["n"] >= 2 and (s["ratio"] > 1.5 or s["hints"] > 1.5)}
    exercises = discover(active_only=False)
    done_lessons = {slugify(r["item"]) for r in read_log() if r["kind"] == "study"}
    skipped = load_profile(required=False).get("skip_modules", [])
    category = {"due": 0, "misconception": 1, "fragile": 2, "gap": 3, "ready": 4, "planned": 6}
    rows = []
    for cid, info in states.items():
        st = info["state"]
        if st not in category or (st in ("gap", "planned") and not info.get("ready")):
            continue
        c = graph["concepts"][cid]
        if cid not in tree and any(c["module"].startswith(m) for m in skipped):
            continue  # a module the learner left out comes back only through an explicit goal
        weak = any(exercises.get(s, {}).get("pattern") in weak_patterns for s in c["exercises"])
        # Due redos and repairs first, then new material in the syllabus's module order (the
        # same order as `today`'s "Next new"); inside a module, weak spots and big unlocks first.
        key = (0 if (not goal or cid in tree) else 1, category[st] + (1 if c["planned"] and st != "planned" else 0),
               c["module"], 0 if weak else 1, -unlocks(graph, states, cid), graph["rank"][cid])
        rows.append((key, cid))
    rows.sort()
    return [(cid, concept_action(graph, cid, states[cid], done_lessons)) for _, cid in rows[:limit]]


def colour(text: str, code: str) -> str:
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return text
    return f"\033[{code}m{text}\033[0m"


def state_tag(state: str) -> str:
    label, code = STATE_STYLE.get(state, (state, "0"))
    return colour(f"{label:9}", code)


def graph_summary(graph: dict, states: dict) -> str:
    counts: dict[str, int] = {}
    for info in states.values():
        counts[info["state"]] = counts.get(info["state"], 0) + 1
    parts = [f"{STATE_STYLE[s][0].rstrip('.')} {counts[s]}" for s in STATE_STYLE if counts.get(s) and s != "unknown"]
    return f"{graph['track']}: {len(states)} concepts ({', '.join(parts) or 'no evidence yet'})"


def graph_brief_line() -> str | None:
    """One line for `today`/`brief`: the graph's state and the top of `graph next`."""
    names = graph_track_names()
    if not names:
        return None
    graph = combined_graph(names)
    _, states = graph_refresh(graph)
    # The redo queue and "Next new" lines already name redos and new exercises: this line adds
    # only what they cannot show, the lessons to take and the concepts to repair.
    top = [(cid, action) for cid, action in graph_next(graph, states, limit=len(states))
           if action.startswith(("teach me", "repair"))][:3]
    line = f"Concept graph, {graph_summary(graph, states)}."
    if top:
        line += " Lessons and repairs next: " + "; ".join(f"{cid} ({action})" for cid, action in top) + "."
    return line


def graph_check(graph: dict) -> tuple[list[str], list[str]]:
    """Errors (the graph is wrong) and warnings (gaps worth closing) for one track's graph."""
    errors: list[str] = []
    warnings: list[str] = []
    data, raw, concepts = graph["data"], graph["raw"], graph["concepts"]
    if data.get("version") != 1:
        errors.append(f"version must be 1 (found {data.get('version')!r})")
    if data.get("track") and data["track"] != graph["track"]:
        errors.append(f"track is '{data['track']}' but the file is in tracks/{graph['track']}/")
    ids = [c.get("id", "") for c in raw]
    for cid in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"duplicate id '{cid}'")
    track_dir = graph["config"]["dir"]
    exercises = {s: ex for s, ex in discover(active_only=False).items() if ex["track"] == graph["track"]}
    topics: dict[str, list[str]] = {}
    for readme in track_dir.glob(f"*/{PRIMM_DIR}/README.md"):
        m = TOPICS_RE.search(readme.read_text(encoding="utf-8"))
        topics[readme.parent.parent.name] = [t.strip() for t in m.group(1).split(", ")] if m else []
    for cid, c in concepts.items():
        where = f"'{cid}'"
        if not GRAPH_ID_RE.match(cid):
            errors.append(f"{where}: ids are lower_snake_case")
        if not c.get("module"):
            errors.append(f"{where}: no module")
        elif not c["planned"] and not (track_dir / c["module"]).is_dir():
            errors.append(f"{where}: module folder {c['module']} does not exist (add \"planned\": true?)")
        if c["kind"] not in ("skill", "theory"):
            errors.append(f"{where}: kind must be skill or theory")
        if not c["can"].strip():
            warnings.append(f"{where}: no 'can' statement (the probe and lessons test it)")
        for r in c["requires"]:
            if r == cid:
                errors.append(f"{where} requires itself")
            elif r not in concepts:
                errors.append(f"{where} requires unknown concept '{r}'")
            elif not c["planned"] and concepts[r]["planned"]:
                warnings.append(f"{where} (built) requires '{r}' from a planned module")
        for slug in c["exercises"]:
            if slug not in exercises:
                errors.append(f"{where}: unknown exercise '{slug}'")
        if c["lesson"] and c["module"] in topics and c["lesson"] not in topics[c["module"]]:
            errors.append(f"{where}: lesson '{c['lesson']}' is not a topic in "
                          f"{c['module']}/{PRIMM_DIR}/README.md")
    for name in load_tracks(active_only=False):
        other = load_graph(name) if name != graph["track"] else None
        for cid, c in concepts.items():
            o = other["concepts"].get(cid) if other else None
            if not o or not (c["shared"] or o["shared"]):
                continue
            if c["shared"] != o["shared"]:
                errors.append(f"'{cid}' is shared in one of {graph['track']} and {name} but not the other: "
                              "a shared id means the same concept in every track")
            elif c["can"] != o["can"] or c["name"] != o["name"]:
                warnings.append(f"shared '{cid}' has a different name or can statement in {name}")
    if graph["cycle"]:
        errors.append("cycle in requires (A -> B: B needs A): " + " -> ".join(reversed(graph["cycle"])))
    covered_lessons = {(c["module"], c["lesson"]) for c in concepts.values() if c["lesson"]}
    for module, names in sorted(topics.items()):
        for t in names:
            if (module, t) not in covered_lessons:
                warnings.append(f"lesson topic '{t}' ({module}) is not the lesson of any concept")
    mapped = set(graph["by_exercise"])
    for slug, ex in exercises.items():
        if slug not in mapped:
            warnings.append(f"exercise '{slug}' ({ex['module']}) belongs to no concept")
    return errors, warnings


def mermaid_text(graph: dict, states: dict) -> str:
    def node(cid: str) -> str:  # Mermaid ids cannot hold the ':' of <track>:<id>
        return cid.replace(":", "__")
    lines = ["flowchart LR"]
    modules: dict[str, list[str]] = {}
    for cid in graph["order"]:
        modules.setdefault(graph["concepts"][cid]["module"], []).append(cid)
    for module, cids in modules.items():
        lines.append(f"  subgraph {module}")
        for cid in cids:
            name = graph["concepts"][cid]["name"].replace('"', "'")
            lines.append(f'    {node(cid)}["{name}"]:::{states[cid]["state"]}')
        lines.append("  end")
    for cid in graph["order"]:
        for r in graph["concepts"][cid]["requires"]:
            if r in graph["concepts"]:
                lines.append(f"  {node(r)} --> {node(cid)}")
    fills = {"fluent": "#2e7d32", "held": "#00838f", "due": "#b8860b", "fragile": "#ef6c00",
             "misconception": "#c62828", "gap": "#ad1457", "ready": "#6a1b9a",
             "unknown": "#9e9e9e", "planned": "#cfcfcf"}
    for state, fill in fills.items():
        text = "#000" if state in ("planned",) else "#fff"
        lines.append(f"  classDef {state} fill:{fill},color:{text},stroke:{fill}")
    return "\n".join(lines)


def graph_layout(graph: dict) -> dict[str, tuple[int, int]]:
    """Layered layout: column = longest prerequisite chain below the concept; rows ordered by
    module, then nudged towards their prerequisites' rows (one barycentre pass)."""
    concepts = graph["concepts"]
    depth: dict[str, int] = {}
    for cid in graph["order"]:
        reqs = [depth[r] for r in concepts[cid]["requires"] if r in depth]
        depth[cid] = 1 + max(reqs) if reqs else 0
    columns: dict[int, list[str]] = {}
    for cid in graph["order"]:
        columns.setdefault(depth[cid], []).append(cid)
    module_rank = {m: i for i, m in enumerate(dict.fromkeys(concepts[c]["module"] for c in graph["order"]))}
    row: dict[str, float] = {}
    for col in sorted(columns):
        cids = columns[col]
        def key(cid: str) -> tuple:
            parents = [row[r] for r in concepts[cid]["requires"] if r in row]
            centre = sum(parents) / len(parents) if parents else module_rank[concepts[cid]["module"]]
            return (centre, module_rank[concepts[cid]["module"]], graph["rank"][cid])
        cids.sort(key=key)
        for i, cid in enumerate(cids):
            row[cid] = i
    return {cid: (depth[cid], int(row[cid])) for cid in concepts}


HTML_TEMPLATE = """<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Concept graph: __TRACK__</title>
<style>
:root{--bg:#fafaf7;--fg:#1d1d1b;--muted:#6b6b66;--panel:#ffffff;--line:#c9c9c2;--edge:#b5b5ad;--hi:#1f6feb;
--fluent:#2e7d32;--held:#00838f;--due:#b8860b;--fragile:#ef6c00;--misconception:#c62828;--gap:#ad1457;--ready:#6a1b9a;--unknown:#8d8d86;--planned:#c4c4bc}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#151514;--fg:#ecece6;--muted:#a3a39b;--panel:#1f1f1d;--line:#3a3a36;--edge:#4b4b46;--hi:#58a6ff;--planned:#4a4a45;--unknown:#77776f}}
:root[data-theme="dark"]{--bg:#151514;--fg:#ecece6;--muted:#a3a39b;--panel:#1f1f1d;--line:#3a3a36;--edge:#4b4b46;--hi:#58a6ff;--planned:#4a4a45;--unknown:#77776f}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
header{padding:16px;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;border-bottom:1px solid var(--line)}
h1{font-size:18px;margin:0}.sum{color:var(--muted);font-size:13px}
.controls{display:flex;flex-wrap:wrap;gap:6px;align-items:center;width:100%}
.chip{border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:999px;padding:3px 10px;font-size:13px;cursor:pointer}
.chip[aria-pressed="false"]{opacity:.45}.chip i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
input[type=search]{flex:1;min-width:140px;max-width:280px;padding:5px 10px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--fg)}
main{display:flex;flex-wrap:wrap;min-height:calc(100vh - 110px)}
#wrap{flex:1 1 600px;min-width:0;overflow:auto;max-height:calc(100vh - 110px)}
aside{flex:0 1 340px;min-width:0;width:100%;max-width:100%;border-left:1px solid var(--line);background:var(--panel);padding:16px;overflow:auto;max-height:calc(100vh - 110px)}
@media (max-width:800px){aside{border-left:0;border-top:1px solid var(--line);flex-basis:100%;max-height:none}#wrap{max-height:70vh}}
svg text{font-size:12px;fill:#fff;pointer-events:none}.node rect{rx:7;stroke-width:2;stroke:transparent;cursor:pointer}
.node.sel rect{stroke:var(--hi);stroke-width:3}.node.dim,.edge.dim{opacity:.13}.edge{fill:none;stroke:var(--edge);stroke-width:1.3}
.edge.hi{stroke:var(--hi);stroke-width:2.2;opacity:1}.node.planned text,.node.unknown text{fill:var(--fg)}
a{color:var(--hi)}aside h2{font-size:16px;margin:0 0 4px}aside .st{font-size:12px;text-transform:uppercase;letter-spacing:.05em}
aside ul{padding-left:18px;margin:4px 0 10px}aside .k{color:var(--muted);font-size:12px;margin-top:10px}
.ev{font-size:13px;border-left:3px solid var(--line);padding-left:8px;margin:6px 0}
#theme{margin-left:auto}
</style></head><body>
<header><h1>Concept graph: __TRACK__</h1><span class="sum">__SUMMARY__ · generated __DATE__</span>
<button class="chip" id="theme" type="button">Theme</button>
<div class="controls" id="filters"><input type="search" id="q" placeholder="Search concepts" aria-label="Search concepts"></div></header>
<main><div id="wrap">__SVG__</div>
<aside id="panel"><h2>Click a concept</h2><p class="sum">Its prerequisites and dependents light up; the panel shows what it lets you do, where it is taught and practised, and your dated evidence.</p>
<p class="sum">Ready = every prerequisite is solid. Due = a redo of one of its exercises is due.</p></aside></main>
<script>
const D=__DATA__;
const states=["fluent","held","due","fragile","misconception","gap","ready","unknown","planned"];
const on=new Set(states);let sel=null;const f=document.getElementById('filters');
states.forEach(s=>{if(!D.counts[s])return;const b=document.createElement('button');b.className='chip';b.type='button';b.setAttribute('aria-pressed','true');
b.innerHTML='<i style="background:var(--'+s+')"></i>'+s+' '+D.counts[s];b.onclick=()=>{on.has(s)?on.delete(s):on.add(s);b.setAttribute('aria-pressed',on.has(s));paint()};f.appendChild(b)});
const q=document.getElementById('q');q.oninput=paint;
function rel(id){const up=new Set(),down=new Set(),walk=(x,k,set)=>{(D.c[x][k]||[]).forEach(y=>{if(!set.has(y)){set.add(y);walk(y,k,set)}})};walk(id,'requires',up);walk(id,'dependents',down);return [up,down]}
function paint(){const t=q.value.trim().toLowerCase();let lit=null;if(sel){const [u,d]=rel(sel);lit=new Set([sel,...u,...d])}
document.querySelectorAll('.node').forEach(n=>{const c=D.c[n.dataset.id];const ok=on.has(c.state)&&(!t||(c.name+' '+n.dataset.id+' '+c.module).toLowerCase().includes(t))&&(!lit||lit.has(n.dataset.id));n.classList.toggle('dim',!ok);n.classList.toggle('sel',n.dataset.id===sel)});
document.querySelectorAll('.edge').forEach(e=>{const a=e.dataset.a,b=e.dataset.b;const hi=lit&&lit.has(a)&&lit.has(b);e.classList.toggle('hi',!!hi);e.classList.toggle('dim',!!lit&&!hi)})}
function esc(s){return String(s).replace(/[&<>"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]))}
function list(xs,fmt){return xs&&xs.length?'<ul>'+xs.map(fmt).join('')+'</ul>':'<p class="sum">none</p>'}
function show(id){sel=sel===id?null:id;paint();if(!sel)return;const c=D.c[id];const p=document.getElementById('panel');
p.innerHTML='<div class="st" style="color:var(--'+c.state+')">'+esc(c.state)+(c.unlocks?' · unlocks '+c.unlocks:'')+'</div><h2>'+esc(c.name)+'</h2><div class="sum">'+esc(c.module)+(c.planned?' (planned)':'')+' · '+esc(c.kind)+'</div>'
+'<div class="k">Can</div><div>'+esc(c.can||'-')+'</div>'+(c.action?'<div class="k">Next step</div><div>'+esc(c.action)+'</div>':'')
+'<div class="k">Needs first</div>'+list(c.requires,x=>'<li><a href="#" data-go="'+x+'">'+esc(D.c[x].name)+'</a> ('+D.c[x].state+')</li>')
+'<div class="k">Leads to</div>'+list(c.dependents,x=>'<li><a href="#" data-go="'+x+'">'+esc(D.c[x].name)+'</a> ('+D.c[x].state+')</li>')
+'<div class="k">Lesson</div><div>'+esc(c.lesson||'-')+'</div><div class="k">Exercises</div>'+list(c.exercises,x=>'<li>'+esc(x)+(c.due.includes(x)?' (redo due)':'')+'</li>')
+'<div class="k">Evidence</div>'+(c.evidence.length?c.evidence.slice().reverse().map(e=>'<div class="ev">'+esc(e.date||'')+' · '+esc(e.state)+' · '+esc(e.source||'')+(e.confidence!==undefined?' · '+esc(e.confidence)+'% sure':'')+(e.note?'<br>'+esc(e.note):'')+'</div>').join(''):'<p class="sum">none yet</p>');
if(innerWidth<=800)p.scrollIntoView({behavior:'smooth',block:'start'});p.querySelectorAll('[data-go]').forEach(a=>a.onclick=ev=>{ev.preventDefault();sel=null;show(a.dataset.go);document.querySelector('.node[data-id="'+a.dataset.go+'"]').scrollIntoView({block:'center',inline:'center',behavior:'smooth'})})}
document.querySelectorAll('.node').forEach(n=>{n.onclick=()=>show(n.dataset.id);n.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();show(n.dataset.id)}}});
document.getElementById('theme').onclick=()=>{const r=document.documentElement;const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=dark?'light':'dark'};
</script></body></html>
"""


def html_text(graph: dict, states: dict) -> str:
    import html as html_mod
    pos = graph_layout(graph)
    w, h, gx, gy, pad = 178, 30, 56, 12, 16
    cols = max((c for c, _ in pos.values()), default=0) + 1
    rows = max((r for _, r in pos.values()), default=0) + 1
    width, height = pad * 2 + cols * w + (cols - 1) * gx, pad * 2 + rows * (h + gy)
    xy = {cid: (pad + c * (w + gx), pad + r * (h + gy)) for cid, (c, r) in pos.items()}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}" role="img" aria-label="Concept graph of {graph["track"]}">']
    for cid in graph["order"]:
        x2, y2 = xy[cid]
        for r in graph["concepts"][cid]["requires"]:
            if r not in xy:
                continue
            x1, y1 = xy[r]
            sx, sy, ex_, ey = x1 + w, y1 + h / 2, x2, y2 + h / 2
            mid = (sx + ex_) / 2
            parts.append(f'<path class="edge" data-a="{r}" data-b="{cid}" '
                         f'd="M{sx:.0f},{sy:.0f} C{mid:.0f},{sy:.0f} {mid:.0f},{ey:.0f} {ex_:.0f},{ey:.0f}"/>')
    for cid in graph["order"]:
        x, y = xy[cid]
        c = graph["concepts"][cid]
        st = states[cid]["state"]
        name = c["name"] if len(c["name"]) <= 26 else c["name"][:25] + "…"
        parts.append(f'<g class="node {st}" data-id="{cid}" tabindex="0" role="button" '
                     f'aria-label="{html_mod.escape(c["name"])}: {st}">'
                     f'<title>{html_mod.escape(c["name"])} ({st})</title>'
                     f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="fill:var(--{st})"/>'
                     f'<text x="{x + 9}" y="{y + 19}">{html_mod.escape(name)}</text></g>')
    parts.append("</svg>")
    done_lessons = {slugify(r["item"]) for r in read_log() if r["kind"] == "study"}
    counts: dict[str, int] = {}
    data = {"c": {}, "counts": counts}
    for cid in graph["order"]:
        c, info = graph["concepts"][cid], states[cid]
        counts[info["state"]] = counts.get(info["state"], 0) + 1
        data["c"][cid] = {
            "name": c["name"], "module": c["module"], "kind": c["kind"], "planned": c["planned"],
            "can": c["can"], "lesson": c["lesson"], "exercises": c["exercises"], "due": info["due"],
            "requires": [r for r in c["requires"] if r in graph["concepts"]],
            "dependents": graph["dependents"][cid], "state": info["state"],
            "unlocks": unlocks(graph, states, cid),
            "action": concept_action(graph, cid, info, done_lessons) if info["state"] not in ("fluent", "held") else "",
            "evidence": info["evidence"],
        }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return (HTML_TEMPLATE.replace("__TRACK__", html_mod.escape(graph["track"]))
            .replace("__SUMMARY__", html_mod.escape(graph_summary(graph, states)))
            .replace("__DATE__", fmt_date(today()))
            .replace("__SVG__", "".join(parts)).replace("__DATA__", payload))


def write_graph_views(graph: dict, states: dict, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    md = out_dir / f"graph_{graph['slug']}.md"
    md.write_text(f"# Concept graph: {graph['track']}\n\n{graph_summary(graph, states)}, "
                  f"{fmt_date(today())}.\n\n```mermaid\n{mermaid_text(graph, states)}\n```\n", encoding="utf-8")
    page = out_dir / f"graph_{graph['slug']}.html"
    page.write_text(html_text(graph, states), encoding="utf-8")
    return [md, page]


def print_graph(graph: dict, states: dict) -> None:
    print(graph_summary(graph, states))
    several = len(graph["parts"]) > 1
    by_module: dict[str, list[str]] = {}
    for cid, c in graph["concepts"].items():  # the order the graph's authors wrote: simplest first
        by_module.setdefault(f"{c['track']}/{c['module']}" if several else c["module"], []).append(cid)
    for module in by_module:
        cids = by_module.get(module, [])
        planned = all(graph["concepts"][c]["planned"] for c in cids)
        print(f"\n{module}" + (" (planned)" if planned else ""))
        for cid in cids:
            c, info = graph["concepts"][cid], states[cid]
            needs = [r for r in c["requires"] if states.get(r, {}).get("state") not in SOLID]
            extra = f"  needs {', '.join(needs)}" if needs and info["state"] not in SOLID else ""
            if info["due"]:
                extra += f"  redo due: {', '.join(info['due'])}"
            if info.get("implied"):
                extra += "  (implied by what builds on it)"
            if c["shared"]:
                extra += "  [shared: counts in every track]"
            print(f"  {state_tag(info['state'])} {cid:26} {c['name']}{extra}")


def cmd_graph(args) -> None:
    """The concept graph: show, path, next, set, derive, check, and views (--html / --mermaid)."""
    action = args.action or "show"
    rest = list(args.args)
    if action not in ("show", "path", "next", "set", "undo", "derive", "check"):
        rest.insert(0, action)  # `graph python` = `graph show python`
        action = "show"
    if action == "check":
        names = rest or [t for t in load_tracks(active_only=False) if load_graph(t)]
        bad = False
        for name in names:
            graph = load_graph(name)
            if not graph:
                print(f"{name}: no {GRAPH_FILE}.")
                continue
            errors, warnings = graph_check(graph)
            print(f"{name}: {len(graph['concepts'])} concepts, {len(errors)} error(s), {len(warnings)} warning(s).")
            for e in errors:
                print(f"  ! {e}")
            for w in warnings if not args.quiet else []:
                print(f"  note: {w}")
            bad = bad or bool(errors)
        if bad:
            sys.exit(1)
        return
    ensure_files()
    if action == "set":
        if len(rest) < 2:
            die("Usage: python dojo.py graph set <concept> <" + "|".join(EVIDENCE_STATES) + "> "
                "[--confidence N] [--source probe] [--note TEXT] [--ref FILE] [--track T]")
        cid, state = rest[0], rest[1]
        graph = pick_graph(args.track)
        if cid not in graph["concepts"]:
            die(f"No concept '{cid}' in the {graph['track']} graph.")
        if state not in EVIDENCE_STATES:
            die(f"State must be one of {', '.join(EVIDENCE_STATES)} (fluent comes from redo boxes).")
        source = args.source or "tutor"
        if source not in EVIDENCE_SOURCES:
            die(f"Source must be one of {', '.join(EVIDENCE_SOURCES)}.")
        overlay = read_overlay()
        entry = {"state": state, "date": fmt_date(today()), "source": source, "note": args.note,
                 "ref": args.ref, "confidence": args.confidence}
        add_evidence(overlay, graph["concepts"][cid], entry)
        write_json(GRAPH_OVERLAY, overlay)
        info = concept_states(graph, overlay, today())[cid]
        print(f"{cid}: {state} ({source}) recorded; state now {info['state']}.")
        return
    if action == "undo":
        if not rest:
            die("Usage: python dojo.py graph undo <concept> [--track T]")
        cid = rest[0]
        graph = pick_graph(args.track)
        if cid not in graph["concepts"]:
            die(f"No concept '{cid}' in the {graph['track']} graph.")
        c = graph["concepts"][cid]
        overlay = read_overlay()
        entries = evidence_of(overlay, c)
        recorded = [i for i, e in enumerate(entries) if not str(e.get("ref", "")).startswith("log:")]
        if not recorded:
            die(f"{cid}: no recorded evidence to undo (evidence read from the log changes only with the log).")
        removed = entries.pop(recorded[-1])
        if not entries:
            del overlay["tracks"][c["store"]][c["local"]]
        write_json(GRAPH_OVERLAY, overlay)
        print(f"{cid}: removed {removed['state']} ({removed.get('source', '')}, {removed.get('date', '')}).")
        return
    graph = pick_graph(args.track if action != "show" else (rest[0] if rest else args.track))
    _, states = graph_refresh(graph, verbose=action == "derive")
    if action == "derive":
        print(graph_summary(graph, states))
        return
    if action == "path":
        if not rest:
            die("Usage: python dojo.py graph path <concept|module|exercise> ...")
        goal = graph_targets(graph, rest)
        tree = graph_ancestors(graph, goal) | set(goal)
        todo = [cid for cid in graph["order"] if cid in tree and states[cid]["state"] not in SOLID]
        held = len(tree) - len(todo)
        print(f"Minimal path to {', '.join(rest)}: {len(todo)} concept(s) to learn, "
              f"{held} already solid and skipped.")
        done_lessons = {slugify(r["item"]) for r in read_log() if r["kind"] == "study"}
        for i, cid in enumerate(todo, 1):
            c = graph["concepts"][cid]
            print(f"  {i:>2}. {state_tag(states[cid]['state'])} {cid:26} {c['module']:24} "
                  f"{concept_action(graph, cid, states[cid], done_lessons)}")
        return
    if action == "next":
        goal = graph_targets(graph, args.goal) if args.goal else None
        items = graph_next(graph, states, goal, limit=args.limit)
        print(f"What can be done now ({graph['track']}" + (f", towards {', '.join(args.goal)}" if goal else "") + "):")
        for cid, act in items:
            info = states[cid]
            n = unlocks(graph, states, cid)
            print(f"  {state_tag(info['state'])} {cid:26} {act}" + (f"  (unlocks {n})" if n else ""))
        if not items:
            print("  nothing ready: every concept is solid or waiting on a prerequisite.")
        return
    print_graph(graph, states)
    if args.html or args.mermaid:
        # exports/ holds only backups (whose zips carry their own views): a view on its own is
        # disposable, so it goes to the system's temporary folder unless --out says otherwise.
        out = Path(args.out).expanduser() if args.out else Path(tempfile.gettempdir()) / "code-dojo"
        for path in write_graph_views(graph, states, out):
            if (path.suffix == ".html" and args.html) or (path.suffix == ".md" and args.mermaid):
                print(f"\nWrote {path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path}")
    top = graph_next(graph, states, limit=3)
    if top:
        print("\nCan do next: " + "; ".join(f"{cid} ({a})" for cid, a in top))
