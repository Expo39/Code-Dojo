"""Move money between two rows, all or nothing.

Level: medium
Target: 30

An `Account` has a `name` and a decimal `balance`. Write `transfer(Account, from_id, to_id, amount)`:

- `amount` must be greater than 0, and `from_id` must differ from `to_id`: otherwise raise
  `ValueError` (before touching the database).
- Take the amount from the first account and add it to the second. If the first account has less
  than `amount`, raise `ValueError("insufficient funds")` and change nothing.
- If either account does not exist, let `Account.DoesNotExist` propagate and change nothing.
- **All or nothing**: if anything fails after the first balance was changed (the second save
  raises, say), the first account's balance must be back as it was. Use a database transaction.
- Lock the two rows while you work on them, so that two transfers at the same time cannot both
  spend the same money.

    Ada 100, Bo 20: transfer(Account, ada.id, bo.id, 30) -> Ada 70, Bo 50

Trace by hand (balances afterwards, or the error):

    Ada 50, Bo 0: transfer(Account, ada.id, bo.id, 80)   -> ?
    Ada 50, Bo 0: transfer(Account, ada.id, ada.id, 10)  -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify transfer_funds
"""

from decimal import Decimal

from django.db import transaction


def transfer(Account, from_id, to_id, amount):
    raise NotImplementedError
