def format_row(*cells, sep=" | ", width=None, **labels):
    parts = []
    for cell in cells:
        text = str(cell)
        if width is not None:
            text = text.ljust(width)
        parts.append(text)
    for name, value in labels.items():
        parts.append(f"{name}={value}")
    return sep.join(parts)
