class Ticket:
    _next_number = 1

    def __init__(self, name):
        self.name = name
        self.number = Ticket._next_number
        Ticket._next_number += 1

    @classmethod
    def reset_numbers(cls):
        cls._next_number = 1


class Queue:
    def __init__(self):
        self._tickets = []

    def take(self, name):
        ticket = Ticket(name)
        self._tickets.append(ticket)
        return ticket

    def serve_next(self):
        if not self._tickets:
            raise IndexError("no one is waiting")
        return self._tickets.pop(0)

    def waiting(self):
        return [ticket.name for ticket in self._tickets]

    def __len__(self):
        return len(self._tickets)
