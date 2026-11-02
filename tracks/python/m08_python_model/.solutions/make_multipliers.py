def make_multipliers(n):
    """Return [f0, f1, ..., f(n-1)] where fi(x) == i * x."""
    return [lambda x, i=i: i * x for i in range(n)]
