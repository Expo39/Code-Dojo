"""Print a bank account number in groups.

Level: easy
Target: 10
Variant of: chunk

An invoice prints the euro bank account number (IBAN) in small groups so
people can read it aloud. Return `code` split into consecutive groups of `size`
characters, separated by single spaces. `code` has no spaces in it.

    format_iban("DE89370400440532", 4) -> "DE89 3704 0044 0532"

Trace by hand (work out the result yourself):

    format_iban("FR7630006000", 5) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify format_iban
"""


def format_iban(code, size):
    raise NotImplementedError
