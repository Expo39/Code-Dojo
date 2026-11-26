def regression_gate(baseline, candidate, max_drop):
    common = sorted(set(baseline) & set(candidate))
    if not common:
        raise ValueError("the two runs share no cases")
    base_rate = sum(1 for c in common if baseline[c]) / len(common)
    cand_rate = sum(1 for c in common if candidate[c]) / len(common)
    return {
        "ok": round(cand_rate, 9) >= round(base_rate - max_drop, 9),
        "baseline": base_rate,
        "candidate": cand_rate,
        "regressed": [c for c in common if baseline[c] and not candidate[c]],
        "new_cases": sorted(set(candidate) - set(baseline)),
        "dropped_cases": sorted(set(baseline) - set(candidate)),
    }
