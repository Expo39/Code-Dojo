# extract_citations: clarifications

Pattern: parse-and-classify

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Ids are matched exactly, including capitals: `[DOC_2]` is not `[doc_2]`.
- A citation is `[` + letters, digits, `_` or `-` (at least one) + `]`; `[]`, `[p 1]` and `[see below]` are not.
- Each id appears once in its list, in order of first appearance in the answer.
- `abstained` is True when the text "not in the documents" appears anywhere, in any capitals.
- An answer can abstain and still cite; report both.
- An empty answer gives empty lists and False.
