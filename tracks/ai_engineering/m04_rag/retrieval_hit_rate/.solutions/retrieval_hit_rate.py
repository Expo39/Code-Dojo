def retrieval_hit_rate(cases, retrieve, k):
    hits = 0
    misses = []
    for case in cases:
        top = retrieve(case["question"])[:max(k, 0)]
        if any(doc in case["relevant"] for doc in top):
            hits += 1
        else:
            misses.append(case["question"])
    total = len(cases)
    return {"hits": hits, "total": total, "rate": hits / total if total else 0.0, "misses": misses}
