"""Same serial number, however it was typed.

Level: easy
Target: 10
Variant of: is_palindrome

Warehouse staff type serial numbers by hand, so the same serial shows up as
"ab-12 cd" in one system and "AB12CD" in another. Return True if `a` and `b` are
the same serial, ignoring case and anything that is not a letter or a digit.

    same_serial("AB-12 cd", "ab12CD") -> True
    same_serial("AB-12", "AB-21") -> False

Trace by hand (work out the result yourself):

    same_serial("x9/7 k.Q", "X97-KQ") -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify same_serial
"""


def same_serial(a, b):
    raise NotImplementedError
