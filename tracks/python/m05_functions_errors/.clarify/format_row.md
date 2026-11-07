# format_row: clarifications

Pattern: varargs-kwargs

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Any value can be a cell (numbers, None, ...): show it with str().
- A second positional argument is just another cell; it never becomes the separator.
- `sep` and `width` must be keyword-only parameters (after `*cells` in the signature).
- Labels keep the order the caller wrote them in, not alphabetical order.
- `width` pads only the cells, never the labels.
- A cell longer than `width` is kept whole, not cut.
- No cells and no labels: return "". Labels only: return just the labels joined by `sep`.
