# Django (placeholder track)

Not built yet, and not part of any plan unless a learner chooses it in their roadmap
(`docs/ROADMAP.md`). When a plan reaches it, the tutor writes `track.json` (`docs/TRACKS.md`)
and generates the first module only. A learner who already has Django material (notes, small
apps, logs) brings it in with `import my notes` first, so the track starts at their real level.

## Prerequisites

- Python fundamentals (the Python track's first milestone), in particular classes, decorators,
  dicts, exceptions, and files and JSON.
- A terminal and a virtual environment.

## Theory (offered just in time, per module)

- HTTP: requests, responses, methods, status codes; safe and idempotent methods (before views).
- Relational databases: tables, keys, joins, grouping, and the SQL behind the ORM (before models).
- The request flow: middleware, URLconf, view, template or serializer (before the first app).
- Authentication against authorisation; sessions and tokens (before login and permissions).

## Outline (fundamentals)

1. Project and app, the request flow, URLs and function views.
2. Templates and static files.
3. Models, migrations and the admin.
4. The ORM: filter, relations (forward and reverse), values, annotate and aggregate, Q and F.
5. Writes: forms and validation, POST, redirects, `get_object_or_404`.
6. Query performance: the N+1 problem, `select_related`, `prefetch_related`.
7. Authentication and permissions.
8. Testing: the test client, `TestCase`, pytest-django.
9. Optional, if the goal needs APIs: Django REST Framework (serializers, viewsets, routers).

Then one small project with no step-by-step guide, chosen for the learner's goal (work, their
own app, or a portfolio piece).

## Toolchain

Django is a Python package: a per-project virtual environment with `pip install django`
(plus `pytest-django` for pytest) is enough. The test command in `track.json` runs the
module's tests with the Django test runner or pytest-django.

## Bridges from Python

Each lesson starts from plain Python the learner knows: a model is a class, a queryset is a lazy
list-like sequence, a view is a function from a request to a response, a decorator wraps a view.
