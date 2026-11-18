# ticket_machine: clarifications

Pattern: class-attribute

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- The counter counts every Ticket created, including ones made directly with Ticket(...) outside a queue.
- Two queues share the same counter, but each queue has its own list of tickets.
- reset_numbers() must be a class method; after it, the next Ticket gets number 1.
- serve_next() on an empty queue raises IndexError.
- Tickets are served in the order they were taken (first in, first out).
- waiting() returns a new list: changing it must not change the queue.
- An empty queue has len 0 and waiting() returns [].
- Queue must not inherit from list.
- Duplicate names are fine: each take gets its own ticket.
