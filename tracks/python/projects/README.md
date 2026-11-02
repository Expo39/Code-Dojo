# Projects

Exercises train single moves; projects train putting them together with nobody telling you
the structure. Each project has a goal, requirements and a "done when" list, but **no
step-by-step guide**: deciding the structure, getting stuck and getting unstuck is the point.

Rules:

- Write it yourself. The tutor answers questions, reviews your design and code
  (`review my project`), and gives hints, but writes none of it.
- Start with the smallest version that runs end to end, then add features one by one.
- Commit to git after every working step (in your own repo or a folder outside this one).
- Write tests for the core logic (from P2 onwards), and a short README explaining how to run it.
- Log the time: `python dojo.py log project 60 P2 --note "added persistence"`.

Code lives in `workspace/projects/<name>/` (personal, gitignored) or in your own repository.

| # | Project | When | Skills |
| --- | --- | --- | --- |
| P1 | Word stats CLI | after m04 | files, parsing, dicts, sorting, command-line arguments |
| P2 | Todo app with storage | after m06 | classes, JSON files, errors, tests |
| P3 | Log analyser | after m11 | parsing real-looking data, aggregation, datetime, a report |
| P4 | Text adventure | early Phase 2 | state machines, data-driven design, a game loop |
| P5 | Inventory or bank system | mid Phase 2 | classes, persistence, validation, a solid test suite |
| P6 | HTTP API client | late Phase 2 | `urllib` or `requests`, JSON, error handling, caching, rate limits |

## P1: Word stats CLI

Goal: `python wordstats.py book.txt --top 10` prints the most common words of a text file.

Requirements: count words case-insensitively without punctuation; `--top N` (default 10);
`--min-length N` to ignore short words; print total words, unique words and the top list as an
aligned table; a clear message (not a traceback) for a missing file.

Done when: works on any `.txt` (try a book from Project Gutenberg); `--help` explains the options
(use `argparse`); you can explain every line.

## P2: Todo app with storage

Goal: a command-line todo list that remembers tasks between runs.

Requirements: `add "title"`, `list` (open tasks, or `--all`), `done <id>`, `remove <id>`;
optional due dates and `list --overdue`; data in a JSON file; a `Task` and a `TodoList` class
kept separate from the command-line code; at least 8 pytest tests of `TodoList`.

Done when: ids are never reused; a corrupted or missing file is handled; tests pass.

## P3: Log analyser

Goal: read a web-server or application log and print a report.

Requirements: parse lines like `2026-11-02T10:00:01 ERROR user=alice path=/api/x 503 120ms`
(fields in any order after the timestamp); report requests per hour, error rate, slowest
paths (median and 95th percentile), and the top users by errors; skip and count malformed
lines; `--since` and `--until` filters; output as text or `--json`.

Done when: a 100,000-line generated log is processed in a few seconds; tests cover parsing
edge cases. (Write a small generator script to create test logs.)

## P4: Text adventure

Goal: a small game of rooms, items and commands (`go north`, `take key`, `inventory`, `use key`).

Requirements: the world is data (a JSON or dict file), not hard-coded `if` chains; a command
parser; save and load; at least one locked door and a win condition.

Done when: a friend can play it to the end without reading the code.

## P5: Inventory or bank system

Goal: a small domain model with rules and persistence, built test-first.

Requirements: products or accounts, movements or transactions, validation with custom
exceptions, a history, reports (low stock, monthly statement), saved in JSON or SQLite
(`sqlite3` is in the standard library); a test suite written before or alongside each feature.

Done when: at least 20 meaningful tests; another person can read the code and understand the
rules from the tests.

## P6: HTTP API client

Goal: a command-line tool around a free public API (weather, public transport, books).

Requirements: request, parse JSON, handle errors and timeouts, cache responses on disk with an
expiry, respect rate limits, configuration from environment variables; tests use saved
responses instead of the network.

Done when: it works offline from the cache, and failures give clear messages.
