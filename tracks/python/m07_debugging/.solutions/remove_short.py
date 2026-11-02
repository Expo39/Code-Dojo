def remove_short(words, min_len):
    """Return a list without the words shorter than min_len. Do not change the input."""
    return [word for word in words if len(word) >= min_len]
