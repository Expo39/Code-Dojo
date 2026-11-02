def q1():
    a = [1, 2]
    b = a
    b.append(3)
    return a


def q2():
    a = [1, 2]
    b = a
    b = b + [3]
    return a


def q3():
    rows = [[0] * 2] * 2
    rows[0][0] = 7
    return rows


def q4():
    def add(x, bucket=[]):
        bucket.append(x)
        return len(bucket)
    add(1)
    add(2)
    return add(3)


def q5():
    s = "abc"
    s.upper()
    return s


PREDICTIONS = {
    "q1": [1, 2, 3],
    "q2": [1, 2],
    "q3": [[7, 0], [7, 0]],
    "q4": 3,
    "q5": 'abc',
}
