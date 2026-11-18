# split_bill: clarifications

Pattern: integer-cents

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- `total` and `tip_percent` can be ints or floats (59.99, 12.5); `tip_percent` 0 means no tip.
- The total with tip is rounded to the nearest cent once, before splitting; the tests never land on exactly half a cent.
- Each share is a float with at most two decimals (38.34, not 38.3333).
- The shares add up exactly to the rounded total; leftover cents go one each to the first people ([38.34, 38.33, 38.33]).
- Amounts a float cannot store exactly (19.99, 0.29) must still come out right to the cent.
- More people than cents: some shares are 0.0.
- `people` 0 or negative: raise ValueError.
