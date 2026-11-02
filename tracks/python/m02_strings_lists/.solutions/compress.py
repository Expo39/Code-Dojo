def compress(text):
    if not text:
        return ""
    parts = []
    current, count = text[0], 1
    for ch in text[1:]:
        if ch == current:
            count += 1
        else:
            parts.append(f"{current}{count}")
            current, count = ch, 1
    parts.append(f"{current}{count}")
    return "".join(parts)
