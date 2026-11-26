# transfer_funds: clarifications

Pattern: atomic-lock

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- `amount` is a number or a `Decimal`; convert with `Decimal(...)` so money never goes through floats.
- Check the amount and the two ids first and raise `ValueError` without opening a transaction or querying.
- A missing account raises `Account.DoesNotExist` (the model's own exception) and nothing changes, whichever of the two is missing.
- An exactly equal balance is fine (the whole balance can be moved); only less than the amount is "insufficient funds".
- The two changes are inside one `transaction.atomic()` block: if the second save raises, the first is rolled back.
- Locking is `select_for_update()` inside the transaction; SQLite ignores it, so the test cannot prove the lock, only that you wrote the transaction. Lock in a fixed order (by id) to avoid deadlocks between opposite transfers.
- Nothing is returned.
