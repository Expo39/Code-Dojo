"""Bank account with a custom exception.

Level: easy
Target: 20

Write class BankAccount(owner, balance=0) with deposit(amount), withdraw(amount),
a `balance` attribute, a `history` list of ("deposit", amount) / ("withdraw", amount)
tuples, and the repr BankAccount('Ann', 50). Also write a custom exception class
InsufficientFunds.

    acc = BankAccount("Ann"); acc.deposit(100); acc.withdraw(30); acc.balance -> 70

Trace by hand (work out the result yourself):

    acc = BankAccount("Bo"); acc.deposit(50); acc.deposit(25); acc.withdraw(40); acc.balance -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify bank_account
"""


class InsufficientFunds(Exception):
    pass


class BankAccount:
    pass
