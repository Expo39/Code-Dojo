# book_model: clarifications

Pattern: model-definition

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- `PositiveIntegerField` allows 0, so the refusal of 0 pages is a database constraint you add yourself (a `CheckConstraint` in `Meta.constraints`; its keyword is `condition` from Django 5.1 and `check` before that).
- `published` must be allowed to be empty in the database (`null=True`) and in forms and `full_clean` (`blank=True`): both are needed.
- `price` is a `DecimalField` with `max_digits=6` and `decimal_places=2`, so `9999.99` is the largest value.
- Default ordering is `Meta.ordering = ["title"]`.
- `__str__` returns exactly `<title> (<isbn>)`; `is_long()` returns a bool, True from 500 pages.
- Keep `app_label = "dojo"` in `Meta`; add to it, do not replace it.
- No migration files are needed: the exercise project builds the table from the model.
