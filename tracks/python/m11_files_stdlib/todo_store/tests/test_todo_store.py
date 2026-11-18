import json
import pytest
from todo_store import TodoStore


def test_add_and_open(tmp_path):
    store = TodoStore(tmp_path / "todo.json")
    assert store.add("milk") == 1
    assert store.add("bread") == 2
    store.complete(1)
    assert store.open_tasks() == ["bread"]


def test_persists(tmp_path):
    path = tmp_path / "todo.json"
    store = TodoStore(path)
    store.add("a")
    store.add("b")
    store.complete(2)
    again = TodoStore(path)
    assert again.open_tasks() == ["a"]
    assert again.add("c") == 3
    assert isinstance(json.loads(path.read_text(encoding="utf-8")), (list, dict))


def test_ids_not_reused(tmp_path):
    store = TodoStore(tmp_path / "t.json")
    store.add("x")
    store.complete(1)
    assert store.add("y") == 2


def test_unknown_id(tmp_path):
    with pytest.raises(KeyError):
        TodoStore(tmp_path / "t.json").complete(99)
