from decimal import Decimal

from django.db import transaction


def transfer(Account, from_id, to_id, amount):
    amount = Decimal(amount)
    if amount <= 0:
        raise ValueError("amount must be positive")
    if from_id == to_id:
        raise ValueError("cannot transfer to the same account")
    with transaction.atomic():
        # lock both rows in a fixed order so two opposite transfers cannot deadlock
        locked = {a.pk: a for a in Account.objects.select_for_update().filter(pk__in=[from_id, to_id]).order_by("pk")}
        if from_id not in locked or to_id not in locked:
            raise Account.DoesNotExist("account not found")
        source, target = locked[from_id], locked[to_id]
        if source.balance < amount:
            raise ValueError("insufficient funds")
        source.balance -= amount
        target.balance += amount
        source.save(update_fields=["balance"])
        target.save(update_fields=["balance"])
