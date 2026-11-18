# shapes: clarifications

Pattern: inheritance

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Square must not define its own area() or perimeter(): it reuses Rectangle's.
- A Square is a Rectangle (isinstance is True).
