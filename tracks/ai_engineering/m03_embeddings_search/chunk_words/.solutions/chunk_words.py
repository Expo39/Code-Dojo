def chunk_words(text, size, overlap):
    if size < 1 or overlap < 0 or overlap >= size:
        raise ValueError("need size >= 1 and 0 <= overlap < size")
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
        start += size - overlap
    return chunks
