"""Fetch a row and its related row in one query.

Level: easy
Target: 15

A `Story` has a `headline` and a foreign key `reporter` to a `Reporter` (who has a `name`).
Write `headlines_with_reporters(Story)`:

- Return a list of strings `"<headline> - <reporter name>"` for every story, in alphabetical order
  of headline.
- Use **one database query** in all, however many stories there are: reading `story.reporter.name`
  in a loop over an ordinary queryset costs one extra query per story.

    stories: ("Floods", Ada), ("Budget", Bo)
    headlines_with_reporters(Story) -> ["Budget - Bo", "Floods - Ada"]

Trace by hand (the list):

    stories: ("Zoo opens", Cy), ("Art fair", Cy), ("Marathon", Di)   -> ?

How many queries would the plain loop `[f"{s.headline} - {s.reporter.name}" for s in Story.objects.all()]`
run for those three stories? Say it before you run anything.

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify headlines_with_reporters
"""


def headlines_with_reporters(Story):
    raise NotImplementedError
