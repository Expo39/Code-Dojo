# cosine_top_k: clarifications

Pattern: cosine-ranking

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Similarity is the cosine as defined: dot product over the product of lengths.
- A vector of all zeros has similarity 0 with everything (no error).
- Items with the same similarity (differences below 1e-9 count as equal) are ordered by id, alphabetically.
- `k` larger than the number of items: return all of them; `k` of 0 or less: an empty list.
- An empty `items` list gives an empty list.
- Vectors are plain Python lists of numbers; no libraries are needed or expected.
- Do not change the inputs.
