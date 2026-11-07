# top_n: clarifications

Pattern: default-args

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- n larger than the list: all items.
- n <= 0: [].
- Type hints: any reasonable types are fine (`list[int]`, `list[Any]`, a `TypeVar`); `n` is an
  `int`, and `key` must allow None (`Callable[..., Any] | None`). The return is annotated too.
- One line of docstring is enough: what it returns.
