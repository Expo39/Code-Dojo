def word_lengths_total(lines):
    """Return {line_number: total letters in that line's words}, numbers from 1."""
    result = {}
    for number, line in enumerate(lines, start=1):
        total = 0
        for word in line.split():
            total += len(word)
        result[number] = total
    return result
