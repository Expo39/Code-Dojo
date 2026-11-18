def count_long_words(words, min_length):
    count = 0
    for word in words:
        if len(word) >= min_length:
            count += 1
    return count
