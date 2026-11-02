"""A decorator.

Level: easy
Target: 15

Write a decorator count_calls. The decorated function works as before and gets
an attribute `.calls` with the number of times it has been called. It keeps the
original function's name and docstring.

    @count_calls
    def hello(): return "hi"
    hello(); hello(); hello.calls -> 2

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify count_calls

Read: https://realpython.com/primer-on-python-decorators/ (first half)
"""


def count_calls(func):
    raise NotImplementedError
