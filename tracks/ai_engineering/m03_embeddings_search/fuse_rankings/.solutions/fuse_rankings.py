def fuse_rankings(rankings, k=60, top=None):
    scores = {}
    for ranking in rankings:
        seen = set()
        place = 0
        for doc in ranking:
            if doc in seen:
                continue
            seen.add(doc)
            place += 1
            scores[doc] = scores.get(doc, 0.0) + 1 / (k + place)
    ordered = sorted(scores, key=lambda d: (-round(scores[d], 9), d))
    return ordered if top is None else ordered[:top]
