# bank_account: clarifications

Pattern: class-state

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- amount must be > 0 for deposit and withdraw, otherwise ValueError.
- Withdrawing more than the balance raises InsufficientFunds and changes nothing (balance and history).
- Each account has its own history.
