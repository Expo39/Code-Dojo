from decimal import Decimal

import pytest
from django.db import models
from transfer_funds import transfer


class Account(models.Model):
    name = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = "dojo"


pytestmark = pytest.mark.django_db


def two(a=100, b=20):
    return (Account.objects.create(name="Ada", balance=Decimal(a)),
            Account.objects.create(name="Bo", balance=Decimal(b)))


def balances(*accounts):
    return [Account.objects.get(pk=a.pk).balance for a in accounts]


def test_a_transfer_moves_the_money():
    ada, bo = two()
    transfer(Account, ada.id, bo.id, 30)
    assert balances(ada, bo) == [Decimal("70"), Decimal("50")]


def test_decimal_amounts_work():
    ada, bo = two()
    transfer(Account, ada.id, bo.id, Decimal("0.01"))
    assert balances(ada, bo) == [Decimal("99.99"), Decimal("20.01")]


def test_insufficient_funds_changes_nothing():
    ada, bo = two(50, 0)
    with pytest.raises(ValueError, match="insufficient funds"):
        transfer(Account, ada.id, bo.id, 80)
    assert balances(ada, bo) == [Decimal("50"), Decimal("0")]


def test_the_whole_balance_can_be_moved():
    ada, bo = two(50, 0)
    transfer(Account, ada.id, bo.id, 50)
    assert balances(ada, bo) == [Decimal("0"), Decimal("50")]


@pytest.mark.parametrize("amount", [0, -5])
def test_non_positive_amounts_are_refused(amount):
    ada, bo = two()
    with pytest.raises(ValueError):
        transfer(Account, ada.id, bo.id, amount)
    assert balances(ada, bo) == [Decimal("100"), Decimal("20")]


def test_the_same_account_is_refused():
    ada, _ = two()
    with pytest.raises(ValueError):
        transfer(Account, ada.id, ada.id, 10)


def test_a_missing_account_changes_nothing():
    ada, _ = two()
    with pytest.raises(Account.DoesNotExist):
        transfer(Account, ada.id, 99999, 10)
    assert balances(ada) == [Decimal("100")]
    with pytest.raises(Account.DoesNotExist):
        transfer(Account, 99999, ada.id, 10)
    assert balances(ada) == [Decimal("100")]


def test_a_failure_after_the_first_change_rolls_it_back(monkeypatch):
    ada, bo = two()
    real_save = Account.save
    calls = []

    def flaky_save(self, *args, **kwargs):
        calls.append(self.pk)
        if len(calls) == 2:
            raise RuntimeError("disk full")
        return real_save(self, *args, **kwargs)

    monkeypatch.setattr(Account, "save", flaky_save)
    with pytest.raises(RuntimeError):
        transfer(Account, ada.id, bo.id, 30)
    monkeypatch.setattr(Account, "save", real_save)
    assert balances(ada, bo) == [Decimal("100"), Decimal("20")]
