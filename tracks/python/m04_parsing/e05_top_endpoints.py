"""Most requested endpoints.

Level: medium
Target: 25
Pattern: parse-count-sort

Each access-log line is: METHOD PATH STATUS DURATION, e.g. "GET /api/users 200 12ms".
Count only successful requests (status 200 to 299). Return the top n paths as a
list of (path, count) tuples, most requests first, ties by path alphabetically.
Skip malformed lines (not exactly 4 fields, or a status that is not a number).

    lines = ["GET /a 200 5ms", "GET /b 200 3ms", "POST /a 201 9ms", "GET /b 500 1ms"]
    top_endpoints(lines, 2) -> [("/a", 2), ("/b", 1)]
"""


def top_endpoints(lines, n):
    raise NotImplementedError
