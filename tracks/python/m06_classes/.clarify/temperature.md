# temperature: clarifications

Pattern: property

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Default reading: 0.0 degrees Celsius.
- No rounding: return the converted value as computed (tests compare approximately).
- Exactly -273.15 is allowed; anything below raises ValueError.
- The constructor applies the same check.
- Assigning a Fahrenheit value that is below absolute zero also raises ValueError.
- A rejected assignment leaves the old reading unchanged.
- Both `celsius` and `fahrenheit` must be properties (not plain attributes or methods).
