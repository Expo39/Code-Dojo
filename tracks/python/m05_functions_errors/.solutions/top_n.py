def top_n(items, n, key=None):
    if n <= 0:
        return []
    return sorted(items, key=key, reverse=True)[:n]
