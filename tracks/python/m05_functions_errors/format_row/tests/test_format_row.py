import inspect

from format_row import format_row


def test_example():
    assert format_row("Ann", 42, "ok", width=4, total=3) == "Ann  | 42   | ok   | total=3"


def test_positional_cells_default_sep():
    assert format_row("a", 1, 2.5, None) == "a | 1 | 2.5 | None"


def test_sep_is_keyword_only():
    # a second positional argument is a cell, never the separator
    assert format_row("x", "-") == "x | -"
    params = inspect.signature(format_row).parameters
    assert params["sep"].kind is inspect.Parameter.KEYWORD_ONLY
    assert params["width"].kind is inspect.Parameter.KEYWORD_ONLY


def test_labels_keep_call_order_and_are_not_padded():
    row = format_row("id", sep=", ", width=3, zeta=1, alpha=True, mid="m")
    assert row == "id , zeta=1, alpha=True, mid=m"


def test_long_cell_not_cut():
    assert format_row("abcdef", "b", width=3) == "abcdef | b  "


def test_empty_and_labels_only():
    assert format_row() == ""
    assert format_row(n=0) == "n=0"
