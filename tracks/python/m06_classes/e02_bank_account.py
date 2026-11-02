"""Bank account with a custom exception.

Level: easy
Target: 20
Pattern: class-state

Write:
- class InsufficientFunds(Exception)
- class BankAccount(owner, balance=0) with:
  - deposit(amount) and withdraw(amount): amount must be > 0 (else ValueError);
    withdrawing more than the balance raises InsufficientFunds and changes nothing
  - balance attribute (read it as account.balance)
  - history: list of ("deposit", amount) / ("withdraw", amount) tuples
  - repr: BankAccount('Ann', 50)
"""


class InsufficientFunds(Exception):
    pass


class BankAccount:
    pass
