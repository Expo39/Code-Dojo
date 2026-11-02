"""Names, objects and mutation.

Level: easy
Target: 10

Kind: predict

READ, do not run. For each question, trace the code by hand (write the
variables on paper, step by step) and put your prediction in PREDICTIONS.
Only then run: python dojo.py test trace_references
The test checks each prediction against what the code really returns.
Wrong ones: find the exact line where your trace went wrong, and say why.
"""

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
    "q1": None,
    "q2": None,
    "q3": None,
    "q4": None,
    "q5": None,
}
