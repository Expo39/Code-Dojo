def split_bill(total, tip_percent, people):
    if people <= 0:
        raise ValueError("people must be at least 1")
    total_cents = round(total * (100 + tip_percent))
    base, leftover = divmod(total_cents, people)
    shares = []
    for i in range(people):
        cents = base + 1 if i < leftover else base
        shares.append(cents / 100)
    return shares
