# word_freq_file: clarifications

Pattern: files

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Words are lower-cased and stripped of . , ! ? ; : " ' ( ) at both ends.
- Ties: alphabetical.
- A missing file raises FileNotFoundError (let Python raise it).
- Non-ASCII words such as "café" must work.
