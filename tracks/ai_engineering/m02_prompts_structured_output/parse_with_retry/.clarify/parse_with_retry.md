# parse_with_retry: clarifications

Pattern: validate-and-retry

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Every call uses the same prompt, unchanged.
- Stop calling the model as soon as a reply is usable; never call it more than
  `max_attempts` times.
- Not JSON at all, or broken JSON: that attempt failed, try again.
- JSON with text around it ("Here you go: {...}"): not usable; do not try to cut the
  JSON out of the text.
- Valid JSON that is not an object (a list, a number, a string): not usable.
- An object missing any required key: not usable. Extra keys are fine and are kept in
  the returned dict.
- No usable reply after `max_attempts` calls: raise ValueError.
- `max_attempts` below 1: raise ValueError without calling the model.
- An empty `required_keys`: any JSON object is usable.
- If the model function itself raises, let the error through.
