"""A view that answers in JSON.

Level: easy
Target: 15

Write the view function `greeting(request)` for a small service:

- It answers `GET` requests with a JSON object `{"message": "Hello, <name>!"}` and status 200.
- `<name>` is the `name` query parameter (`/?name=Ada`) with surrounding spaces removed. When the
  parameter is missing or blank, use `world`.
- Any other HTTP method gets the standard "405 Method Not Allowed" response, and its `Allow`
  header says which method is allowed.

    GET /?name=Ada      -> 200 {"message": "Hello, Ada!"}
    GET /               -> 200 {"message": "Hello, world!"}
    POST /              -> 405, Allow: GET

Trace by hand (status and body):

    GET /?name=%20%20Grace%20Hopper%20  (the name is "  Grace Hopper ")   -> ?
    GET /?name=                                                           -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify json_greeting
"""

from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.http import require_GET


def greeting(request):
    raise NotImplementedError
