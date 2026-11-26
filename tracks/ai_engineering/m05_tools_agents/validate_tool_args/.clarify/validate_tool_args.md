# validate_tool_args: clarifications

Pattern: validate-and-report-all

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Report every problem at once, not only the first.
- Order: schema names in schema order (missing, then wrong type, per name), then unknown arguments in the order of `args`.
- A missing optional argument is fine; a present argument is always type-checked, including None (type name `NoneType`).
- A bool is never accepted for `int` or `float`; an int is accepted for `float` but a float is not accepted for `int`.
- The type name in the message is the real Python type name (`str`, `int`, `float`, `bool`, `NoneType`, `list`, ...).
- Do not change the inputs; an empty list means valid.
