# split_names: clarifications

Pattern: bulk-data-migration

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Words are split on any whitespace, so extra spaces inside or around the name do not matter.
- A one-word name gives only a first name; the last name stays empty.
- A `full_name` that is empty or only spaces has no words: skip it, do not count it, leave both columns empty.
- People whose `first_name` is already filled are never touched, which is also what makes a second run change nobody.
- Return the number of people actually changed (not the number looked at).
- At most 2 queries means one to read and one to write (`bulk_update`), not one save per person; `bulk_update` with no objects does no query.
- The function takes the model as an argument because inside a migration you must use the historical model from `apps.get_model`, never an import.
