import argparse
import sys
from collections import Counter
from pathlib import Path

PUNCTUATION = ".,!?;:\"'()"


def positive_int(text):
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("must be 1 or more")
    return value


def build_parser():
    parser = argparse.ArgumentParser(description="Count the words in a text file.")
    parser.add_argument("path", help="UTF-8 text file to read")
    parser.add_argument("--top", type=positive_int, default=3, help="words to list")
    parser.add_argument("--ignore-case", action="store_true", help="lower-case words")
    return parser


def main(argv):
    args = build_parser().parse_args(argv)
    text = Path(args.path).read_text(encoding="utf-8")
    words = [w.strip(PUNCTUATION) for w in text.split()]
    words = [w for w in words if w]
    if args.ignore_case:
        words = [w.lower() for w in words]
    counts = Counter(words)
    ranked = sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))[: args.top]
    lines = [f"words: {len(words)}", f"unique: {len(counts)}"]
    lines += [f"{word} {count}" for word, count in ranked]
    return "\n".join(lines)


if __name__ == "__main__":
    print(main(sys.argv[1:]))
