def parse_duration(text):
    seconds_per = {"h": 3600, "m": 60, "s": 1}
    order = "hms"
    total = 0
    digits = ""
    last_unit = -1
    for ch in text:
        if ch.isdigit():
            digits += ch
        elif ch in seconds_per:
            position = order.index(ch)
            if not digits or position <= last_unit:
                raise ValueError(f"bad duration: {text!r}")
            total += int(digits) * seconds_per[ch]
            digits = ""
            last_unit = position
        else:
            raise ValueError(f"bad character {ch!r} in {text!r}")
    if digits or last_unit == -1:
        raise ValueError(f"bad duration: {text!r}")
    return total
