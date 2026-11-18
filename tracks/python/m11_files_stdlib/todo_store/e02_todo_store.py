"""Save and load JSON.

Level: easy
Target: 20

Write class TodoStore(path) with add(title) -> int (adds an open task and returns
its id), complete(task_id), and open_tasks() -> the titles not done, in id order.
Every change is saved to the JSON file at `path` immediately; a new TodoStore on
the same path sees the saved tasks.

    store = TodoStore("todo.json"); store.add("milk") -> 1; store.add("bread") -> 2

Trace by hand (work out the result yourself):

    store = TodoStore("t.json"); store.add("eggs"); store.add("tea"); store.complete(1)
    TodoStore("t.json").open_tasks() -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify todo_store

Read: https://docs.python.org/3/library/json.html (json.load, json.dump)
"""


class TodoStore:
    pass
