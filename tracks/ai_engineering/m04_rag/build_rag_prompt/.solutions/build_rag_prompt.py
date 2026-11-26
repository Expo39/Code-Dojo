INSTRUCTION = (
    "Answer using only the passages below. Cite passage ids in square brackets, like [p1]. "
    "If the passages do not contain the answer, say: not in the documents."
)


def build_rag_prompt(question, passages, max_words):
    ranked = sorted(passages, key=lambda p: -p["score"])  # a stable sort keeps input order on ties
    used = []
    total = 0
    for p in ranked:
        words = len(p["text"].split())
        if total + words <= max_words:
            used.append(p)
            total += words
    parts = [INSTRUCTION]
    if used:
        parts.append("\n".join(f"[{p['id']}] {p['text']}" for p in used))
    parts.append(f"Question: {question}\nAnswer:")
    return "\n\n".join(parts), [p["id"] for p in used]
