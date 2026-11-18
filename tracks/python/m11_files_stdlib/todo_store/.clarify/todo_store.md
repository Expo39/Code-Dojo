# todo_store: clarifications

Pattern: json-files

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Ids start at 1 and are never reused, even after reloading from the file.
- complete() with an unknown id raises KeyError.
- A missing file means no tasks yet.
