"""A data migration step: fill new columns from old data.

Level: medium
Target: 25

A `Person` table has `full_name`, and two new empty columns, `first_name` and `last_name`. A data
migration (a `RunPython` step) must fill them. Write `split_names(Person)`; it receives the model
class (in a real migration: `apps.get_model("app", "Person")`) and:

- Handles the people whose `first_name` is empty and whose `full_name` has at least one word
  (words are separated by any whitespace).
- With one word, that word is the `first_name` and the `last_name` stays empty. With more words, the
  last word is the `last_name` and everything before it (joined by single spaces) is the `first_name`.
- Returns how many people it changed. Running it twice changes nobody the second time.
- It must be cheap on a big table: at most **2 database queries** however many people there are.

    "Ada Lovelace" -> first "Ada", last "Lovelace"        "Cher" -> first "Cher", last ""
    "Mary Ann Smith" -> first "Mary Ann", last "Smith"

Trace by hand (first, last and the number returned), for the table
`["  Alan   Turing ", "Plato", "", "Grace Brewster Murray Hopper"]` with all first names empty:

    split_names(Person) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify split_names
"""


def split_names(Person):
    raise NotImplementedError
