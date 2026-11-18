import json
from pathlib import Path


class TodoStore:
    def __init__(self, path):
        self.path = Path(path)
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.tasks = data["tasks"]
            self.next_id = data["next_id"]
        else:
            self.tasks = []
            self.next_id = 1

    def _save(self):
        data = {"tasks": self.tasks, "next_id": self.next_id}
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add(self, title):
        task_id = self.next_id
        self.tasks.append({"id": task_id, "title": title, "done": False})
        self.next_id += 1
        self._save()
        return task_id

    def complete(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["done"] = True
                self._save()
                return
        raise KeyError(task_id)

    def open_tasks(self):
        return [t["title"] for t in self.tasks if not t["done"]]
