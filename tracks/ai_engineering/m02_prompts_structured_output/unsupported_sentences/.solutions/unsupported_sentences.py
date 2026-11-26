import re

STOPWORDS = {"a", "an", "the", "we", "are", "is", "of", "to", "in", "and", "or", "it", "this", "that",
             "for", "on", "with", "as", "be"}


def content_words(text):
    return [w for w in re.findall("[a-z0-9]+", text.lower()) if w not in STOPWORDS]


def unsupported_sentences(answer, passages, min_overlap):
    sources = [set(content_words(p)) for p in passages]
    flagged = []
    for sentence in re.split(r"(?<=[.!?])\s+", answer.strip()):
        sentence = sentence.strip()
        if not sentence:
            continue
        words = content_words(sentence)
        if not words:
            continue
        best = max((sum(1 for w in words if w in src) / len(words) for src in sources), default=0.0)
        if round(best, 9) < round(min_overlap, 9):
            flagged.append(sentence)
    return flagged
