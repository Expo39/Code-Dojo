"""Describe a table as a Django model.

Level: medium
Target: 25

Finish the model `Book` (leave `class Meta: app_label = "dojo"` as it is, the exercise project needs
it). A library wants:

- `title`: text up to 200 characters;
- `isbn`: text up to 13 characters, unique;
- `pages`: a positive whole number, and the database itself must refuse 0 pages;
- `published`: a date that may be empty (in the database and in forms);
- `price`: a decimal number with at most 6 digits in all, 2 of them after the point;
- books are listed ordered by title by default;
- `str(book)` is `"<title> (<isbn>)"`;
- a method `is_long()` that is True for 500 pages or more.

    Book(title="Dune", isbn="9780441013593", pages=412, price=Decimal("9.99"))
    str(...)    -> "Dune (9780441013593)"        .is_long() -> False

Trace by hand (what happens?):

    Book.objects.create(title="A", isbn="1", pages=0, price=Decimal("1"))     -> ?
    Book(title="A", isbn="1", pages=10, price=Decimal("10000.00")).full_clean() -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify book_model
"""

from django.db import models


class Book(models.Model):
    class Meta:
        app_label = "dojo"
