"""Drop short words (buggy).

Level: easy
Target: 10

Kind: debug

The function below has ONE bug (sometimes two lines). Do not rewrite it.
1. Read it and predict the bug before running anything. Say it out loud.
2. Run the tests: python dojo.py test remove_short
3. Confirm with the debugger: a breakpoint (or breakpoint()) and inspect the variables.
4. Fix it with the smallest change and name the bug class.
"""


def remove_short(words, min_len):
    """Return a list without the words shorter than min_len. Do not change the input."""
    for word in words:
        if len(word) < min_len:
            words.remove(word)
    return words
