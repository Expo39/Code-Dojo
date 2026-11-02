def most_common_char(text):
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    best = None
    for ch in text:
        if best is None or counts[ch] > counts[best]:
            best = ch
    return best
