"""Ask again until the model's JSON is usable.

Level: easy
Target: 15

You ask a model to extract invoice fields from an email and to answer in JSON. Models
sometimes answer with chatty text, broken JSON, or JSON that lacks a field. Write
`parse_with_retry(model, prompt, required_keys, max_attempts)`:

- `model` is a function: `model(prompt)` returns the model's reply as a string.
- Call it with `prompt`, up to `max_attempts` times. Return the first reply that parses
  as a JSON object holding every key in `required_keys`, as a dict.
- If no reply is usable after `max_attempts` calls, raise ValueError.
- Use the json module to decide whether a reply is usable, not string checks.

    replies = iter([
        'Sure! Here are the fields you asked for.',
        '{"supplier": "Acme Tools", "total_eur": 120.5, "date": "03/11/2026"}',
    ])
    model = lambda prompt: next(replies)

    parse_with_retry(model, "Extract supplier, total_eur and date.",
                     ["supplier", "total_eur", "date"], 3)
    -> {"supplier": "Acme Tools", "total_eur": 120.5, "date": "03/11/2026"}

Trace by hand (work out the result yourself, and how many times the model is called):

    replies = iter([
        '{"city": "Lyon"',
        '["Lyon", 12]',
        '{"city": "Lyon", "temp_c": 12}',
        '{"city": "Nice"}',
    ])
    parse_with_retry(lambda prompt: next(replies), "Weather as JSON.",
                     ["city", "temp_c"], 4) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify parse_with_retry
"""

import json


def parse_with_retry(model, prompt, required_keys, max_attempts):
    raise NotImplementedError
