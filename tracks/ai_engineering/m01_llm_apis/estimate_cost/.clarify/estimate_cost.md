# estimate_cost: clarifications

Pattern: rate-table-lookup

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Cost = each token count times its price, divided by 1,000,000, summed over the three
  kinds; the total is rounded to cents (2 decimals) once, at the end.
- Cache-read tokens use their own (lower) price and are not also counted as input.
- All counts zero: 0 (0.0 is fine).
- A model that is not in the table: raise ValueError naming the model; do not guess a price.
- A negative token count: raise ValueError.
- Every model in the table has all three prices; counts are whole numbers.
- `prices` is not changed.
