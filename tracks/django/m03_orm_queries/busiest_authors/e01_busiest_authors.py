"""Count related rows in the database, not in Python.

Level: medium
Target: 25

A `Writer` has many `Novel` rows (`writer.novels`, the related name of the foreign key). Write
`busiest_authors(Writer, min_novels, limit)`:

- Return a list of `(name, count)` tuples for the writers with at least `min_novels` novels,
  where `count` is their number of novels.
- Most novels first; writers with the same count in alphabetical order of name.
- At most `limit` tuples (`limit` 0 or less: an empty list).
- Do it in **one query**, however many writers there are: let the database count and filter.

    writers: Ada (3 novels), Bo (1), Cy (3), Di (0)
    busiest_authors(Writer, 1, 10) -> [("Ada", 3), ("Cy", 3), ("Bo", 1)]

Trace by hand:

    writers: Eve (2 novels), Fay (5), Gus (2), Hal (4);  busiest_authors(Writer, 2, 3) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify busiest_authors
"""

from django.db.models import Count


def busiest_authors(Writer, min_novels, limit):
    raise NotImplementedError
