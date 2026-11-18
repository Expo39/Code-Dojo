"""Squash repeated log messages.

Level: easy
Target: 15
Variant of: compress

A server log repeats the same message many times in a row. Return a new list
where each run of identical consecutive messages becomes one entry: the message
itself when it appears once, or "<message> (xN)" when it appears N times in a row.
Do not change `lines`.

    squash_repeats(["boot", "ping", "ping", "ping", "halt"])
    -> ["boot", "ping (x3)", "halt"]

Trace by hand (work out the result yourself):

    squash_repeats(["disk ok", "disk ok", "fan on", "disk ok", "disk ok"]) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify squash_repeats
"""


def squash_repeats(lines):
    raise NotImplementedError
