def rank_scores(records):
    return sorted(records, key=lambda r: (-r[1], r[0]))
