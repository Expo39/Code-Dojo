from collections import Counter
from pathlib import Path


def word_freq_file(path, n):
    text = Path(path).read_text(encoding="utf-8")
    words = [w.strip(".,!?;:\"'()").lower() for w in text.split()]
    counts = Counter(w for w in words if w)
    return sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))[:n]
