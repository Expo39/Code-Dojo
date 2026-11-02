"""Save and load JSON.

Level: easy
Target: 20
Pattern: json-files

class TodoStore(path):
- add(title) -> int: adds an open task, returns its id (1, 2, 3 ... never reused)
- complete(task_id): marks it done; unknown id raises KeyError
- open_tasks() -> list of titles not done, in id order
- every change is saved to the JSON file at `path` immediately, and a new
  TodoStore on the same path sees the saved tasks. A missing file = no tasks.

Read: https://docs.python.org/3/library/json.html (json.load, json.dump)
"""


class TodoStore:
    pass
