def shortest_word(words):
    if not words:
        return None
    best = words[0]
    for word in words[1:]:
        if len(word) < len(best):
            best = word
    return best
