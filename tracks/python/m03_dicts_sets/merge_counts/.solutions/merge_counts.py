def merge_counts(a, b):
    result = dict(a)
    for key, count in b.items():
        result[key] = result.get(key, 0) + count
    return result
