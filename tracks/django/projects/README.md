# Projects

Exercises train single moves; projects put them together with nobody telling you the structure. Each project has a
goal, requirements and a "done when" list, but **no step-by-step guide**.

Rules:

- Write it yourself. The tutor answers questions, reviews your design and code (`review my project`) and gives
  hints, but writes none of it.
- Start with the smallest version that runs end to end, then add one feature at a time.
- Commit to git after every working step, in your own repository. Settings and secrets come from the
  environment, never from the code.
- Write tests for the core logic (queries, validation, permissions) and assert the number of queries on list pages.
- Log the time: `python dojo.py log project 60 P1 --note "added the admin"`.

Code lives in `workspace/django/projects/<name>/` (personal, gitignored) or in your own repository.

| # | Project | When | Skills |
| --- | --- | --- | --- |
| P1 | A small library site | after m04 | models, migrations, admin, forms, generic views, tests |
| P2 | A notes API | after m08 | authentication, permissions, DRF, filtering, OpenAPI, query-count tests |
| P3 | Capstone: a multi-user app | after m12 | structure, a task after commit, a WebSocket notice, containers, deployment |

## P1: A small library site

Goal: members browse books and authors, borrow and return books, and staff manage the catalogue.

Requirements: models for authors, books and loans with constraints that stop a book being lent twice at once;
list and detail pages with pagination; a form to borrow with validation; the admin configured for staff; a custom
user model from the start; tests for the constraints, the forms and the pages.

Done when: borrowing the same copy twice at the same moment cannot succeed (you can say why), a list page runs a
fixed number of queries however many books exist, and a stranger can run it from the README.

## P2: A notes API

Goal: a JSON API for users' private notes with tags and sharing.

Requirements: token authentication; a note is visible only to its owner and the people it is shared with
(enforced in the queryset and in a permission); filtering, search and pagination; validation errors with
consistent shape; an OpenAPI schema and docs page; tests as an authenticated user, as another user and as an
anonymous client.

Done when: no endpoint can leak another user's note (prove it with tests), list endpoints have a query-count
test, and the schema is the contract you test against.

## P3: Capstone: a multi-user app

Goal: P1 or P2 extended with something that happens later and live: an email or export done by a background task,
and a notice pushed to the browser over a WebSocket.

Requirements: services and selectors for the business logic; settings per environment; a task enqueued only
after the transaction commits, safe to run twice; a WebSocket consumer that authenticates the user and checks
the origin; a Compose stack (web, worker, scheduler if needed, database, Redis); a README with the architecture,
the release steps and the backup and restore steps; deployed with lab 12.1.

Done when: killing the worker mid-task loses nothing, a release with a migration happens with no downtime for the
old version, a restored backup gives the same data, and you can say what it costs a day to run.
