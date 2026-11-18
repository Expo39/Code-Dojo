def q1():
    return {w: len(w) for w in ["hi", "yo", "hey", "hi"]}


def q2():
    people = [("ann", 30), ("bob", 25), ("cat", 30)]
    return [name for name, age in sorted(people, key=lambda p: (-p[1], p[0]))]


def q3():
    gen = (x * x for x in range(4))
    first = sum(gen)
    second = sum(gen)
    return (first, second)


def q4():
    return list(zip("abc", [1, 2]))


def q5():
    return sorted("banana", reverse=True)[:3]


PREDICTIONS = {
    "q1": {'hi': 2, 'yo': 2, 'hey': 3},
    "q2": ['ann', 'cat', 'bob'],
    "q3": (14, 0),
    "q4": [('a', 1), ('b', 2)],
    "q5": ['n', 'n', 'b'],
}
