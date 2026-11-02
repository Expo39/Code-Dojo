from rate_limiter import RateLimiter


def test_example():
    rl = RateLimiter(2, 10)
    assert rl.allow("a", 0) is True
    assert rl.allow("a", 1) is True
    assert rl.allow("a", 2) is False
    assert rl.allow("a", 10.5) is True


def test_rejected_calls_do_not_count():
    rl = RateLimiter(1, 10)
    assert rl.allow("a", 0)
    assert not rl.allow("a", 5)
    assert rl.allow("a", 10.1)


def test_users_independent():
    rl = RateLimiter(1, 60)
    assert rl.allow("a", 0)
    assert rl.allow("b", 0)
    assert not rl.allow("a", 1)


def test_boundary_expired():
    rl = RateLimiter(1, 10)
    assert rl.allow("a", 0)
    assert rl.allow("a", 10)
