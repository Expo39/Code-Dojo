import pytest
from parse_with_retry import parse_with_retry

KEYS = ["supplier", "total_eur", "date"]
GOOD = '{"supplier": "Acme Tools", "total_eur": 120.5, "date": "03/11/2026"}'


class FakeModel:
    """Returns the scripted replies in order and records every prompt it gets."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        return self.replies[len(self.prompts) - 1]


def test_example_second_reply_usable():
    model = FakeModel(["Sure! Here are the fields you asked for.", GOOD])
    result = parse_with_retry(model, "Extract supplier, total_eur and date.", KEYS, 3)
    assert result == {"supplier": "Acme Tools", "total_eur": 120.5, "date": "03/11/2026"}
    assert model.prompts == ["Extract supplier, total_eur and date."] * 2


def test_stops_at_first_usable_reply():
    model = FakeModel([GOOD, "never used", "never used"])
    assert parse_with_retry(model, "p", KEYS, 3)["supplier"] == "Acme Tools"
    assert len(model.prompts) == 1


def test_wrong_shapes_and_missing_keys_are_retried():
    model = FakeModel([
        '["Acme Tools", 120.5]',
        '{"supplier": "Acme Tools", "total_eur": 120.5}',
        'Here you go: ' + GOOD,
        '{"supplier": "B", "total_eur": 9, "date": "01/01/2026", "currency": "EUR"}',
    ])
    result = parse_with_retry(model, "p", KEYS, 4)
    assert result == {"supplier": "B", "total_eur": 9, "date": "01/01/2026", "currency": "EUR"}
    assert len(model.prompts) == 4


def test_gives_up_after_max_attempts():
    model = FakeModel(['{"supplier": "A"', "no", "{}", GOOD])
    with pytest.raises(ValueError):
        parse_with_retry(model, "p", KEYS, 3)
    assert len(model.prompts) == 3


def test_zero_attempts_raises_without_calling():
    model = FakeModel([GOOD])
    with pytest.raises(ValueError):
        parse_with_retry(model, "p", KEYS, 0)
    assert model.prompts == []
