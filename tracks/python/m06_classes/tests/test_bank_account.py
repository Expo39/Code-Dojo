import pytest
from bank_account import BankAccount, InsufficientFunds


def test_deposit_withdraw():
    acc = BankAccount("Ann")
    acc.deposit(100)
    acc.withdraw(30)
    assert acc.balance == 70
    assert acc.history == [("deposit", 100), ("withdraw", 30)]


def test_overdraw():
    acc = BankAccount("Ann", 10)
    with pytest.raises(InsufficientFunds):
        acc.withdraw(11)
    assert acc.balance == 10
    assert acc.history == []


def test_bad_amounts():
    acc = BankAccount("Ann")
    with pytest.raises(ValueError):
        acc.deposit(0)
    with pytest.raises(ValueError):
        acc.withdraw(-5)


def test_repr_and_separate_history():
    a, b = BankAccount("Ann", 50), BankAccount("Bo")
    a.deposit(1)
    assert repr(BankAccount("Ann", 50)) == "BankAccount('Ann', 50)"
    assert b.history == []
