def first_index(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1
