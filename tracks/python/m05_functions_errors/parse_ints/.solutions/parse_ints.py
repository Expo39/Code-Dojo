def parse_ints(items):
    numbers, errors = [], []
    for item in items:
        try:
            numbers.append(int(item))
        except ValueError:
            errors.append(item)
    return numbers, errors
