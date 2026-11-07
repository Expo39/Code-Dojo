"""Deli counter ticket machine.

Level: medium
Target: 20

A deli counter hands out numbered tickets. Write two classes.

Ticket(name): has `name` and `number`. Numbers start at 1 and go up by one for
every Ticket created anywhere in the program, whichever queue it is in. The class
keeps that counter itself, and the class method Ticket.reset_numbers() starts it
again from 1.

Queue(): holds the waiting Tickets in a list of its own (a Queue is not a kind of
list; it has one). Methods:
- take(name): create a Ticket for that customer, add it to the back, return it.
- serve_next(): remove the Ticket at the front and return it.
- waiting(): the waiting customers' names, front first, as a new list.
- len(queue) gives the number of waiting tickets.

    q = Queue(); q.take("Ann"); q.take("Bo"); q.serve_next().number -> 1; q.waiting() -> ["Bo"]

Trace by hand (work out the result yourself):

    Ticket.reset_numbers(); a = Queue(); b = Queue(); a.take("Cy"); b.take("Di"); a.take("Ed");
    a.serve_next(); b.take("Fay"); [t.number for t in (b.serve_next(), a.serve_next())] -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify ticket_machine
"""


class Ticket:
    def __init__(self, name):
        raise NotImplementedError


class Queue:
    def __init__(self):
        raise NotImplementedError
