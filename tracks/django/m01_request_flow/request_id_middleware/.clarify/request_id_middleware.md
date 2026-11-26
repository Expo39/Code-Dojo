# request_id_middleware: clarifications

Pattern: middleware-wrapper

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- The header arrives in `request.META` as `HTTP_X_REQUEST_ID`.
- Stripping happens first: `"  req_9  "` becomes `req_9` and is kept.
- Allowed characters are ASCII letters, digits, `-` and `_` only, 1 to 64 of them; anything else (spaces inside, other punctuation, non-ASCII, control characters) is replaced.
- A replaced or missing id is `uuid.uuid4().hex`: 32 lower-case hex characters.
- `request.request_id` is set before `get_response` is called, so views and later middleware can use it.
- The response body and status are not changed; only the header is added.
- No settings or database are involved; the class is plain Python around Django's request and response.
