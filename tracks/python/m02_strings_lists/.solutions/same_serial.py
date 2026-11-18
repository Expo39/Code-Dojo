def clean(text):
    return "".join(ch.lower() for ch in text if ch.isalnum())


def same_serial(a, b):
    return clean(a) == clean(b)
