def make_counter(start=0):
    current = start

    def counter():
        nonlocal current
        value = current
        current += 1
        return value

    return counter
