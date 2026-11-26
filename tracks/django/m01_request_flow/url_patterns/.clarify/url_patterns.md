# url_patterns: clarifications

Pattern: url-routing

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- The names in the table are exact, including the hyphen in `article-detail`.
- An integer converter matches digits only, so a negative number (`-1`) and `7a` do not match either.
- The slug converter accepts letters, digits, hyphens and underscores, not spaces.
- Each URL ends with a slash, as in the table; do not add other URLs.
- Use `path()` with converters; regular expressions (`re_path`) are not needed.
- A request that matches no pattern is a 404 raised by the URL resolver, not by your views.
