# inventory: clarifications

Pattern: class-dict

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- qty must be > 0 for add and remove, otherwise ValueError.
- Removing more than is in stock (or an unknown item): ValueError, and nothing changes.
- An item that reaches 0 disappears.
- count of an unknown item: 0.
- low_stock returns a sorted list.
