from errors_by_user import errors_by_user

LOG = """2026-10-23 10:00:01 ERROR user=alice disk full
2026-10-23 10:00:02 user=bob INFO login
2026-10-23 10:00:03 user=alice ERROR timeout
2026-10-23 10:00:04 user=bob ERROR crash
2026-10-23 10:00:05 ERROR no user here
"""


def test_example():
    assert errors_by_user(LOG) == {"alice": 2, "bob": 1}


def test_user_before_level():
    assert errors_by_user("user=carol x ERROR") == {"carol": 1}


def test_no_errors():
    assert errors_by_user("user=a INFO\nuser=b WARN") == {}


def test_empty():
    assert errors_by_user("") == {}
