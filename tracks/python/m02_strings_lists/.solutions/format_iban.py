def format_iban(code, size):
    if size < 1:
        raise ValueError("size must be at least 1")
    groups = [code[i:i + size] for i in range(0, len(code), size)]
    return " ".join(groups)
