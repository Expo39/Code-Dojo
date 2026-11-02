def invert_dict(d):
    result = {}
    for key, value in d.items():
        result.setdefault(value, []).append(key)
    return {value: sorted(keys) for value, keys in result.items()}
