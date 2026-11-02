"""A decorator.

Level: easy
Target: 15
Pattern: decorator

Write a decorator count_calls. The decorated function works as before and gets
an attribute `.calls` with the number of times it has been called. Keep the
original name and docstring (functools.wraps).

    @count_calls
    def hello(): return "hi"
    hello(); hello(); hello.calls -> 2

Read: https://realpython.com/primer-on-python-decorators/ (first half)
"""


def count_calls(func):
    raise NotImplementedError
