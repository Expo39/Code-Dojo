def last_n(items, n):
    """Return the last n items (all of them if n >= len). n <= 0 gives []."""
    if n <= 0:
        return []
    start = max(len(items) - n, 0)
    return items[start:]
