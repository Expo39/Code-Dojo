def dedupe(items):
    """Return items without duplicates, keeping the first occurrence order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
