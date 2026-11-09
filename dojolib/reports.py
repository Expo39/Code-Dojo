"""Reports: today and the brief, the week, stats, modules and the mix."""

from __future__ import annotations

from datetime import timedelta

from .core import (
    FILE_DATE_FMT, MASTERED_BOX, MISTAKES, PROFILE, PROGRESS, REVIEWS, ROOT, SESSION, TIMER, WEEKLY, die,
    fmt_date, fmt_min, load_profile, parse_date, planned_minutes, read_json, today, week_start,
    weekly_target, write_json
)
from .data import due_items, minutes_on, read_log, session_gap, timer_minutes, timer_of
from .tracks import discover, load_tracks
from .planning import (
    calibration, effective_mix, fluency_gates, interleave_due, next_new, print_modules,
    recent_stats, session_size, strand_line, week_numbers
)
from .graph import graph_brief_line
from .updates import changes_lines, daily_upstream_check, track_changes, upstream_behind
from .migrate import is_dated_row


def cmd_modules(args) -> None:
    """Show the learner's modules; the tutor goes through them with the learner (dojo-assess)."""
    print_modules(load_profile())
    print("Leave one out: python dojo.py settings skip_modules+=<module>; add one back: skip_modules-=<module>.")


def cmd_mix(args) -> None:
    """Show or set the share of new-material time per track, and the current priority."""
    profile = load_profile()
    available = load_tracks(active_only=False)
    mix = effective_mix(profile)
    if args.shares:
        for share in args.shares:
            name, _, value = share.partition("=")
            if name not in available or not value.isdigit():
                die(f"Use track=percent with one of: {', '.join(available)} (got '{share}').")
            mix[name] = int(value)
            if name not in profile["tracks"]:
                profile["tracks"] = list(profile["tracks"] or load_tracks(active_only=True)) + [name]
        if sum(mix.values()) != 100:
            die("The shares must add up to 100 (0 = maintenance). Would be: "
                + ", ".join(f"{t}={v}" for t, v in mix.items()))
        profile["mix"] = mix
    if args.priority is not None:
        profile["priority"] = args.priority
    if args.shares or args.priority is not None:
        write_json(PROFILE, profile)
        print("Saved. Record the reason under 'Plan changes' in progress/PLAN.md.")
    for name, value in mix.items():
        state = "maintenance (redos only)" if value == 0 else f"{value}% of new material"
        print(f"  {name:12} {state}")
        if args.shares and value > 0 and available[name]["requires"]:
            print("    requires: " + "; ".join(available[name]["requires"]))
    print(f"Priority: {profile.get('priority') or '(none)'}")


def cmd_today(args, brief: bool = False) -> None:
    profile = load_profile(required=not brief)
    if not PROFILE.exists():
        print("[dojo] New learner, no profile yet: offer to set them up in chat (dojo-assess, step 0),\n"
              "or they run `python dojo.py setup` in a terminal.")
        return
    rows = read_log()
    on = today()
    plan = planned_minutes(profile, on)
    done_today = minutes_on(rows, on)
    wk = week_numbers(profile, rows, on)
    due = interleave_due(due_items(on))
    timers = read_json(TIMER, {})
    mix = effective_mix(profile)
    upcoming = next_new(profile)

    lines = []
    day_name = on.strftime("%A %d %B %Y")
    lines.append(f"{day_name}: {fmt_min(done_today)} of {fmt_min(plan)} planned today"
                 + (" (rest day)" if plan == 0 else "") + ".")
    gap = wk["gap"]
    status = "on track" if gap >= -15 else f"behind by {fmt_min(-gap)}"
    if gap > 15:
        status = f"ahead by {fmt_min(gap)}"
    lines.append(f"This week: {fmt_min(wk['done'])} of {fmt_min(wk['target'])} ({status}).")
    if gap < -15 and wk["remaining_days"]:
        days = wk["remaining_days"]
        extra = min(-gap / len(days), 60)
        names = ", ".join("today" if d == on else d.strftime("%A") for d in days)
        line = f"  Catch-up: add about {fmt_min(extra)} on each of: {names}"
        if profile["flexible_rest_day"]:
            line += " (or train on the rest day)"
        left = -gap - extra * len(days)
        if left > 15:
            line += (f". About {fmt_min(left)} will stay open this week: let it go, "
                     "it does not carry over.")
        lines.append(line + ("" if left > 15 else "."))
    if wk["prev_gap"] < -60 and on.weekday() < 2:
        lines.append(f"  Last week finished {fmt_min(-wk['prev_gap'])} short. Do not try to repay it all; "
                     "prioritise the redo queue this week.")
    if profile.get("target_date"):
        days_left = (parse_date(profile["target_date"]) - on).days
        if days_left >= 0:
            lines.append(f"Target date {profile['target_date']}: {days_left} days left.")
    balance = strand_line(profile, rows, on)
    if balance:
        lines.append(balance)
    session = read_json(SESSION, None)
    if session:
        clock, logged, gap = session_gap(session, rows)
        lines.append(f"Session clock: {fmt_min(clock)}{' (PAUSED)' if session['paused_at'] else ''}; "
                     f"{fmt_min(gap)} outside timers is added as study at `session end`.")
    if timers:
        lines.append("Timers running: " + ", ".join(
            f"{k} ({fmt_min(timer_minutes(v))} so far{', PAUSED' if timer_of(v)['paused_at'] else ''})"
            for k, v in timers.items()))
    if due:
        names = ", ".join(f"{k} (box {v['box']})" for k, v in due[:8])
        more = f" and {len(due) - 8} more" if len(due) > 8 else ""
        lines.append(f"Redo queue ({len(due)} due, in interleaved order): {names}{more}.")
    else:
        lines.append("Redo queue: nothing due.")
    if profile.get("mode") or profile.get("target_level"):
        lines.append("Mode: " + (profile.get("mode") or "not set")
                     + ", target level: " + (profile.get("target_level") or "not set") + ".")
    if profile.get("priority"):
        lines.append(f"Priority: {profile['priority']}.")
    if len(mix) > 1:
        lines.append("Mix: " + ", ".join(
            f"{t} maintenance (redos only)" if v == 0
            else f"{t} {v}%" + (f" (about {fmt_min(plan * v / 100)} of today)" if plan else "")
            for t, v in mix.items()) + ".")
        for t, v in mix.items():
            items = next_new(profile, track=t) if v > 0 else []
            if items:
                lines.append(f"Next new ({t}): " + ", ".join(f"{e['slug']} ({e['module']})" for e in items) + ".")
    elif upcoming:
        lines.append("Next new: " + ", ".join(f"{e['slug']} ({e['module']})" for e in upcoming) + ".")
    weak = [(p, s) for p, s in recent_stats(rows, 14, on).items()
            if s["n"] >= 2 and (s["ratio"] > 1.5 or s["hints"] > 1.5)]
    if weak:
        lines.append("Weak spots (last 14 days): " + ", ".join(
            f"{p} ({s['ratio']:.1f}x, {s['hints']:.1f} hints)" for p, s in weak[:5]) + ".")
    graph_line = graph_brief_line()
    if graph_line:
        lines.append(graph_line)
    changes = changes_lines(track_changes())
    if changes:
        lines.append("Track changes to ask about (learn it / already know it / not for me): "
                     + " | ".join(changes) + ". Details: `python dojo.py changes`.")
    behind = daily_upstream_check() if brief else upstream_behind(fetch=False)
    if behind:
        lines.append(f"Updates on the shared repo: {behind} new commit(s). Say `update` "
                     "or run `python dojo.py update`.")
    if brief:
        print("[dojo status, from `python dojo.py brief`]")
    print("\n".join(lines))
    if not brief:
        print("\nSession plan for today: see docs/DAILY_SESSION.md "
              f"(the {session_size(plan)} version).")


def cmd_week(args) -> None:
    profile = load_profile()
    rows = read_log()
    on = parse_date(args.date) if args.date else today()
    start = week_start(on)
    end = start + timedelta(days=6)
    wk_rows = [r for r in rows if start <= parse_date(r["date"]) <= end]
    total = sum(float(r["minutes"] or 0) for r in wk_rows)
    target = weekly_target(profile)
    by_kind: dict[str, float] = {}
    for r in wk_rows:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + float(r["minutes"] or 0)
    per_day = [(start + timedelta(days=i)) for i in range(7)]
    stats = recent_stats(rows, (on - start).days + 1, on)
    attempts = [r for r in wk_rows if r["kind"] in ("exercise", "external")]
    solved = [r for r in attempts if r["result"] == "solved"]
    clean = [r for r in solved if int(r["hints"] or 0) == 0 and r["ratio"] and float(r["ratio"]) <= 1.0]
    reviews = read_json(REVIEWS, {})
    mastered = sum(1 for c in reviews.values() if c["box"] >= MASTERED_BOX)
    mistakes = [line for log in [MISTAKES, *sorted(PROGRESS.glob("*/mistakes.md"))] if log.exists()
                for line in log.read_text(encoding="utf-8").splitlines()
                if is_dated_row(line) and start <= parse_date(line.split("|")[1]) <= end]

    iso = on.isocalendar()
    out = [f"# Week {iso[1]} of {iso[0]} ({fmt_date(start)} to {fmt_date(end)})", ""]
    pct = 100 * total / target if target else 0
    out.append(f"**Time:** {fmt_min(total)} of {fmt_min(target)} ({pct:.0f}%).")
    out.append("")
    out.append("| Day | Planned | Done |")
    out.append("| --- | --- | --- |")
    for d in per_day:
        out.append(f"| {d.strftime('%a %d')} | {fmt_min(planned_minutes(profile, d))} | {fmt_min(minutes_on(rows, d))} |")
    out.append("")
    out.append("**By activity:** " + (", ".join(f"{k} {fmt_min(v)}" for k, v in sorted(by_kind.items())) or "none"))
    out.append("")
    out.append(f"**Problems:** {len(attempts)} attempted, {len(solved)} solved, "
               f"{len(clean)} clean (no hints, within target). Mastered items overall: {mastered}.")
    out.append("")
    if stats:
        out.append("| Pattern | Attempts | Median time ratio | Avg hints | Clean |")
        out.append("| --- | --- | --- | --- | --- |")
        for p, s in sorted(stats.items(), key=lambda kv: -kv[1]["ratio"]):
            out.append(f"| {p} | {s['n']} | {s['ratio']:.2f}x | {s['hints']:.1f} | {s['clean']} |")
        out.append("")
    tracked = [r for r in attempts if "skipped" in r]
    if tracked:
        full = sum(1 for r in tracked if not r.get("skipped"))
        counts: dict[str, int] = {}
        for r in tracked:
            for step in filter(None, (r.get("skipped") or "").split(",")):
                counts[step] = counts.get(step, 0) + 1
        line = f"**Process:** every step followed in {full} of {len(tracked)} attempts ({100 * full / len(tracked):.0f}%)."
        if counts:
            line += " Most skipped: " + ", ".join(f"{k} ({v})" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])) + "."
        out.append(line)
        out.append("")
    out.append(f"**Mistakes logged:** {len(mistakes)}")
    out.extend(mistakes)
    out.append("")
    out.append("## Coach notes")
    out.append("")
    out.append("_Filled in by the tutor during the weekly review (`/dojo-weekly`)._")
    text = "\n".join(out) + "\n"
    print(text)
    if args.write:
        WEEKLY.mkdir(parents=True, exist_ok=True)
        path = WEEKLY / f"week_{start.strftime(FILE_DATE_FMT)}.md"
        if path.exists() and not args.force:
            print(f"{path.relative_to(ROOT)} exists; pass --force to overwrite.")
        else:
            path.write_text(text, encoding="utf-8")
            print(f"Written to {path.relative_to(ROOT)}")


def cmd_stats(args) -> None:
    rows = read_log()
    on = today()
    exercises = discover()
    reviews = read_json(REVIEWS, {})
    total = sum(float(r["minutes"] or 0) for r in rows)
    print(f"Total logged: {fmt_min(total)} over {len({r['date'] for r in rows})} days.\n")
    print("Modules (exercises tried / total, mastered):")
    modules: dict[str, list[str]] = {}
    for slug, ex in exercises.items():
        modules.setdefault(f"{ex['track']}/{ex['module']}", []).append(slug)
    for name, slugs in modules.items():
        tried = sum(1 for s in slugs if s in reviews)
        mastered = sum(1 for s in slugs if reviews.get(s, {}).get("box", 0) >= MASTERED_BOX)
        print(f"  {name:40} {tried:>2}/{len(slugs):<2} mastered {mastered}")
    mix = effective_mix(load_profile(required=False))
    if len(mix) > 1:
        module_track = {ex["module"]: ex["track"] for ex in exercises.values()}
        since = on - timedelta(days=28)
        spent: dict[str, float] = {}
        for r in rows:
            if parse_date(r["date"]) > since and r["module"] in module_track:
                t = module_track[r["module"]]
                spent[t] = spent.get(t, 0.0) + float(r["minutes"] or 0)
        total_t = sum(spent.values()) or 1
        print("Track time, last 28 days (exercises and lessons with a module) against the mix:")
        for t, v in mix.items():
            print(f"  {t:12} {fmt_min(spent.get(t, 0))} ({100 * spent.get(t, 0) / total_t:.0f}%), mix {v}%")
        print()
    print("\nLast 28 days by pattern:")
    for p, s in sorted(recent_stats(rows, 28, on).items(), key=lambda kv: -kv[1]["ratio"]):
        print(f"  {p:28} n={s['n']:<3} median {s['ratio']:.2f}x  hints {s['hints']:.1f}  clean {s['clean']}")
    calibrated = calibration(rows)
    if calibrated:
        print("\nConfidence against results (predictions and answers with a stated confidence):")
        print("\n".join(calibrated))
    print("\nFluency gates (see the track README, section 'Milestones'):")
    for label, check in fluency_gates(rows, on):
        print(f"  [{'x' if check else ' '}] {label}")
