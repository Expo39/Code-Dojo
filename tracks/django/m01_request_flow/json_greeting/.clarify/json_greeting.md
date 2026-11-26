# json_greeting: clarifications

Pattern: view-contract

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- `GET` only; `HEAD`, `POST`, `PUT`, `DELETE` and the rest are all 405 (HEAD is not special here).
- The 405 response is Django's standard one: status 405 with an `Allow: GET` header; the body does not matter.
- Only leading and trailing spaces are removed from the name; spaces inside it stay.
- A missing parameter, an empty one and one of only spaces all mean `world`.
- The response is JSON with the usual JSON content type; non-ASCII names are fine.
- If the parameter is repeated (`?name=a&name=b`), use the last one, as Django's `request.GET.get` does.
