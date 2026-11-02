def q1():
    total = 0
    for i in range(1, 10, 3):
        total += i
    return total


def q2(items):
    return items[1:-1][::-1]


def q3(n):
    result = []
    while n > 1:
        result.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    return result


def q4(words):
    out = {}
    for i, w in enumerate(words):
        out[w[0]] = i
    return out


PREDICTIONS = {
    "q1": 12,
    "q2": [4, 3, 2],
    "q3": [6, 3, 10, 5, 16, 8, 4, 2],
    "q4": {'a': 1, 'b': 3, 'c': 4},
}
