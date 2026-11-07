import typing

from summarise_scores import summarise_scores


def test_example():
    assert summarise_scores([6.0, 9.0, 7.5], pass_mark=7.0) == {
        "mean": 7.5, "best": 9.0, "worst": 6.0, "pass_rate": 0.67,
    }


def test_no_pass_mark_and_boundary_counts_as_pass():
    assert summarise_scores([5.0, 5.0, 2.0]) == {
        "mean": 4.0, "best": 5.0, "worst": 2.0, "pass_rate": None,
    }
    assert summarise_scores([5.0, 4.0], pass_mark=5.0)["pass_rate"] == 0.5


def test_empty_list_gives_none_values():
    assert summarise_scores([], pass_mark=3.0) == {
        "mean": None, "best": None, "worst": None, "pass_rate": None,
    }


def test_input_unchanged():
    data = [3.0, 1.0, 2.0]
    summarise_scores(data, pass_mark=2.0)
    assert data == [3.0, 1.0, 2.0]


def test_fully_annotated():
    hints = typing.get_type_hints(summarise_scores)
    assert hints.get("scores") == list[float]
    assert hints.get("pass_mark") == float | None
    assert hints.get("return") == dict[str, float | None]


def test_has_docstring():
    assert summarise_scores.__doc__ and summarise_scores.__doc__.strip()
