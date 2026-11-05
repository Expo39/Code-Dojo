"""Most requested endpoints.

Level: medium
Target: 25

Each access-log line is METHOD PATH STATUS DURATION, e.g. "GET /api/users 200 12ms".
Return the n most requested paths as (path, count) tuples, most requests first.

    lines = ["GET /a 200 5ms", "GET /b 200 3ms", "POST /a 201 9ms", "GET /b 500 1ms"]
    top_endpoints(lines, 2) -> [("/a", 2), ("/b", 1)]

Trace by hand (work out the result yourself):

    lines = ["GET /x 200 4ms", "GET /y 200 2ms", "GET /x 404 1ms",
             "PUT /z 200 7ms", "GET /y 200 3ms", "GET /x 200 3ms"]
    top_endpoints(lines, 2) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify top_endpoints
"""


def top_endpoints(lines, n):
    raise NotImplementedError
