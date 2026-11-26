"""A middleware that tags every request with an id.

Level: medium
Target: 20

When something fails in production you need to find every log line of one request. Write the
middleware class `RequestIDMiddleware` (the "new style": `__init__(self, get_response)` and
`__call__(self, request)`):

- Read the `X-Request-ID` request header. Keep its value when it is non-empty after stripping
  spaces, at most 64 characters, and made only of letters, digits, `-` and `_`.
- Otherwise make a new id: `uuid.uuid4().hex`.
- Store the id on `request.request_id` before the view runs.
- Call `get_response(request)`, set the `X-Request-ID` header of the response to the same id, and
  return the response.

    request with header "X-Request-ID: abc-123"  -> request.request_id == "abc-123" and the response header is "abc-123"
    request without the header                   -> a 32-character hex id, different each time

Trace by hand (kept or replaced?):

    "  req_9  "    -> ?        "has space"    -> ?        "x" * 65    -> ?        "ok-1"    -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify request_id_middleware
"""

import re
import uuid


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        raise NotImplementedError
