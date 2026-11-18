"""One row of a plain-text table.

Level: easy
Target: 15

Write format_row(*cells, sep=" | ", width=None, **labels) that builds one row of a
plain-text report and returns it as a string.

- Every positional argument is a cell, shown with str().
- `sep` goes between neighbouring parts of the row.
- When `width` is given, each cell is padded on the right with spaces to that width.
- Every extra keyword argument is a label, added after the cells as "name=value",
  in the order the caller wrote them.
- `sep` and `width` can only be passed by keyword.

    format_row("Ann", 42, "ok", width=4, total=3) -> "Ann  | 42   | ok   | total=3"

Trace by hand (work out the result yourself):

    format_row("id", 7, "red", "big", sep=", ", done=True) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify format_row
"""


def format_row(*cells, sep=" | ", width=None, **labels):
    raise NotImplementedError
