import pytest
from run_tool_loop import run_tool_loop


class Script:
    """A fake model: returns scripted replies and records a copy of the messages it was shown."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.seen = []

    def __call__(self, messages):
        self.seen.append(list(messages))
        return self.replies[len(self.seen) - 1]


def test_example_one_tool_then_final():
    model = Script([{"tool": "add", "args": {"a": 2, "b": 3}}, {"final": "5"}])
    result = run_tool_loop(model, {"add": lambda a, b: a + b}, "2+3?", 5)
    assert result["answer"] == "5" and result["steps"] == 2 and result["stopped"] == "final"
    assert result["messages"] == [
        {"role": "user", "content": "2+3?"},
        {"role": "tool", "name": "add", "content": "5"},
    ]


def test_the_model_sees_the_tool_result_on_its_next_turn():
    model = Script([{"tool": "add", "args": {"a": 1, "b": 1}}, {"final": "x"}])
    run_tool_loop(model, {"add": lambda a, b: a + b}, "q", 3)
    assert len(model.seen[0]) == 1 and len(model.seen[1]) == 2
    assert model.seen[1][-1] == {"role": "tool", "name": "add", "content": "2"}


def test_trace_a_failing_tool_then_a_second_call_hits_the_limit():
    model = Script([{"tool": "div", "args": {"a": 1, "b": 0}}, {"tool": "div", "args": {"a": 4, "b": 2}},
                    {"final": "done"}])
    result = run_tool_loop(model, {"div": lambda a, b: a / b}, "go", 2)
    assert result["stopped"] == "step limit" and result["answer"] is None and result["steps"] == 2
    assert result["messages"][1]["content"] == "error: division by zero"
    assert result["messages"][2]["content"] == "2.0"


def test_unknown_tool_is_reported_to_the_model_and_the_loop_goes_on():
    model = Script([{"tool": "nope", "args": {}}, {"final": "gave up"}])
    result = run_tool_loop(model, {}, "q", 3)
    assert result["messages"][1] == {"role": "tool", "name": "nope", "content": "error: unknown tool nope"}
    assert result["answer"] == "gave up" and result["steps"] == 2


def test_final_on_the_first_call():
    result = run_tool_loop(Script([{"final": "hi"}]), {}, "q", 1)
    assert result == {"answer": "hi", "steps": 1, "stopped": "final", "messages": [{"role": "user", "content": "q"}]}


def test_final_on_the_last_allowed_step_still_counts():
    model = Script([{"tool": "t", "args": {}}, {"final": "ok"}])
    result = run_tool_loop(model, {"t": lambda: "r"}, "q", 2)
    assert result["stopped"] == "final" and result["answer"] == "ok"


def test_max_steps_below_one_raises_without_calling_the_model():
    model = Script([{"final": "x"}])
    with pytest.raises(ValueError):
        run_tool_loop(model, {}, "q", 0)
    assert model.seen == []
