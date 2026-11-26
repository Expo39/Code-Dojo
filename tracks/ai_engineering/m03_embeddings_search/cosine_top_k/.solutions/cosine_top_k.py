import math


def cosine_top_k(query, items, k):
    if k <= 0:
        return []
    q_len = math.sqrt(sum(x * x for x in query))
    scored = []
    for item_id, vector in items:
        v_len = math.sqrt(sum(x * x for x in vector))
        if q_len == 0 or v_len == 0:
            score = 0.0
        else:
            score = sum(a * b for a, b in zip(query, vector)) / (q_len * v_len)
        scored.append((round(score, 9), item_id))
    scored.sort(key=lambda s: (-s[0], s[1]))
    return [item_id for _, item_id in scored[:k]]
