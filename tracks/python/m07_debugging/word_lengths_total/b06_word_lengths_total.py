"""Total characters across lines (buggy).

Level: easy
Target: 10

Kind: debug

The function below has ONE bug (sometimes two lines). Do not rewrite it.
1. Read it and predict the bug before running anything. Say it out loud.
2. Run the tests: python dojo.py test word_lengths_total
3. Confirm with the debugger: a breakpoint (or breakpoint()) and inspect the variables.
4. Fix it with the smallest change and name the bug class.
"""


def word_lengths_total(lines):
    """Return {line_number: total letters in that line's words}, numbers from 1."""
    result = {}
    for number, line in enumerate(lines, start=1):
        total = 0
        for word in line.split():
            total = len(word)
        result[number] = total
    return result
