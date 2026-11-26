# headlines_with_reporters: clarifications

Pattern: select-related

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Every story has exactly one reporter (the foreign key is required).
- Sort by headline in the database or in Python: only the order of the result matters.
- The result must hold every story, one string each, in the format `<headline> - <reporter name>`.
- The test counts queries: one in total, including the loop that builds the strings.
- The plain loop over `Story.objects.all()` runs 1 query for the stories plus 1 per story for its reporter: 4 for three stories (the classic N+1 problem).
