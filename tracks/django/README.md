# Django track

Last reviewed: 26 November 2026, against Django 6.1 (current; it needs Python 3.12 or newer), with notes for
codebases still on Django 4.2 LTS (its security support ended in April 2026, so every module says what differs
and `VERSIONS.md` has the upgrade path), Django REST framework 3.16, Celery 5, Channels 4 and the sources under
"Sources". Builds on the Python track.

How to build and run server-side web applications and APIs with Django: the request cycle, models and the ORM,
forms, authentication and security, testing, performance, REST APIs, project structure, real time with
WebSockets, background work with Celery, and operating a Django system (containers, proxy, backups, upgrades,
a cloud deployment). One of the tracks a learner can choose; nothing here is compulsory.

Not covered, on purpose: internationalisation, GeoDjango and CMS packages (specialist areas); front-end
JavaScript frameworks (a different subject); packaging reusable apps and contributing to Django; and other
Python web frameworks, except where a module compares them in a few lines.

## Prerequisites

Python fluency: classes, decorators, dicts, exceptions, JSON, modules and a little `pytest` (the first milestone
of the Python track). A terminal. The exercises need `django` and `pytest-django` in the project's virtual
environment: `python dojo.py install` installs them (the track's `requirements.txt`) when Django is one of your
tracks. Try-it tasks and labs use SQLite, or PostgreSQL and Redis in containers.

## How lessons work in this track

Most concepts start from a **source you read yourself**, then a recall, then questions, then a build:

1. **Read** the source named under "Read first" (one stretch at a time).
2. **Recall**: close it and say, in your own words, the three to five points that matter, one concrete example
   and one thing you would push back on.
3. **Questions**: the module's `discussion.md`, answered out loud; the tutor follows up and scores the answer.
4. **Build it**, in three sizes: a short **exercise** (modules 1 to 3 have them: a small piece of a real Django
   app, tested offline against a bundled SQLite project in `_project/`), the module's `try_it.md` tasks, and a
   **project** in `projects/`. Module 12 also has real-account **labs** (`labs.md`) with a cost estimate.
5. **Revise** from the module's `explainers/` where it has them.

`teach me <topic>` (PRIMM) is used where code behaviour is the point. Each block stays inside its own steps
(`docs/CHECKLISTS.md`, section 8); anything else that comes up is noted and offered afterwards.

## Modules

| Module | Focus | Status |
| --- | --- | --- |
| m01_request_flow | HTTP, project and app layout, the request cycle, URL routing, function views, middleware, templates, static files | seeded |
| m02_models_migrations | relational basics, models and fields, relationships, the migration workflow, data migrations, the admin | seeded |
| m03_orm_queries | QuerySets, lookups, Q and F, aggregation, following relations, bulk operations, transactions and locking, raw SQL | seeded |
| m04_forms_class_views | forms and validation, model forms, post/redirect/get, class-based and generic views | planned |
| m05_auth_security | authentication, a custom user model, permissions, sessions, web security, login limits | planned |
| m06_testing | the test client, pytest-django, query-count tests, testing forms and models, isolation | planned |
| m07_performance | the N+1 problem, indexes, caching, pagination, precomputed rollups, profiling | planned |
| m08_rest_apis | REST basics, serializers, API views and viewsets, API authentication, filtering, errors and versioning, OpenAPI, testing | planned |
| m09_project_structure | app boundaries, settings, services and selectors, managers, signals, management commands, feature flags, audit trails, error handling | planned |
| m10_async_realtime | ASGI, async views, Channels consumers, channel layers, WebSocket authentication, choosing a real-time technique | planned |
| m11_background_work | Celery with Django, retries and idempotency, enqueue after commit, beat, the outbox pattern, queues, Django's Tasks, monitoring | planned |
| m12_operations_deployment | Compose stacks, application servers, reverse proxy and HTTPS, static and media, migrations in a release, backups, logging, secrets, upgrading Django, cloud deployment | planned |

Every module has its concepts, lesson topics, discussion questions and try-it tasks; modules marked planned
have no exercises yet, which are written when a learner reaches them (`dojo-new-exercise`). Projects are in
`projects/`; labs are in `m12_operations_deployment/labs.md` and `labs/README.md`.

## Read first, per module

- **m01**: the Django tutorial, parts 1, 3 and 6; the MDN Django module (introduction, skeleton website, home
  page); the Django documentation's topic guides on URLs, views, middleware and templates. Optional beginner
  on-ramp: the Django Girls tutorial.
- **m02**: the Django tutorial, parts 2 and 7; MDN, "Using models" and "Django admin site"; the topic guides on
  models and migrations.
- **m03**: the topic guide "Making queries" (all of it); the guides on aggregation, database transactions and
  raw SQL; Django Girls, "Django ORM and QuerySets".
- **m04**: the Django tutorial, part 4; MDN, "Working with forms" and "Generic list and detail views"; the topic
  guides on forms and class-based views.
- **m05**: the topic guides "Using the Django authentication system", "Security in Django" and "Sessions"; MDN,
  "User authentication and permissions" and "Django web application security"; CS50 Web, weeks 3 and 8.
- **m06**: the Django tutorial, part 5; the topic guide "Writing and running tests"; MDN, "Testing a Django web
  application"; the pytest-django documentation; CS50 Web, week 7.
- **m07**: the topic guides "Performance and optimization", "Database access optimization" and "Django's cache
  framework"; the debug toolbar's documentation.
- **m08**: the Django REST framework home page, quickstart and tutorial parts 1 to 6, then its API guide for
  serializers, permissions, filtering, pagination and testing; the drf-spectacular documentation; HackSoft's
  Django Styleguide, the chapter on APIs and serializers.
- **m09**: HackSoft's Django Styleguide (models, services, selectors, settings, errors, testing); the topic guide
  on signals; the documentation of `django-admin` and of django-waffle.
- **m10**: the Django topic guide "Asynchronous support" and the ASGI deployment guide; the Channels
  documentation: its four-part tutorial, then consumers, routing, channel layers, authentication, security and
  testing.
- **m11**: Celery's "First steps with Django" and its documentation on tasks, routing and periodic tasks;
  HackSoft's Django Styleguide, the chapter on Celery; the Django 6.0 release notes on background tasks.
- **m12**: the Django deployment checklist and the guides to deploying with ASGI and WSGI; MDN, "Deploying
  Django to production"; CS50 Web, weeks 7 and 8; the Django release notes from your version to the newest.

## Theory (offered just in time, per module)

- m01: HTTP: requests, responses, methods, status codes, safe and idempotent methods.
- m02: relational databases: tables, keys, joins, indexes, constraints.
- m08: REST: resources, methods, statelessness, idempotency, and the alternatives.
- m10: WSGI and ASGI; what an event loop does.

## Bar

Able to build, with no scaffold other than Django itself, a multi-user web application with a JSON API: models and
migrations (including a data migration), forms or serializers with validation, authentication with permissions,
queries with no N+1, a test suite that runs against a real database (including query counts), a background task
enqueued safely after commit, and a containerised deployment with its settings and secrets outside the code; and
to explain each choice (a signal or a service call, a cache or an index, a task or a request, async or sync) with
a measurement or a trade-off.

## Left out, and why

- Internationalisation, GeoDjango, CMS packages: specialist areas that need their own track.
- Front-end JavaScript frameworks and CSS: another subject; templates are taught as far as server-side work needs.
- Reusable-app packaging and contributing to Django: not needed to build and run applications.
- Other Python web frameworks: compared in a few lines (module 1), not taught.

## Where this track departs from its sources

- Tutorials build one small app (a poll, a library). This track adds what a running system needs and tutorials
  skip: transactions and locking, query performance, project structure, background work, real time and
  operations. Most of those come from the official topic guides and the practitioner guide (HackSoft's
  Styleguide, which is the only source for services and selectors) rather than from any course.
- Courses stop at "deploy to a platform". Module 12 teaches release migrations, backups, upgrades and cost, and
  gives real-account labs with the cost estimated first.
- Exercises are small slices of a real app tested offline, so the engineering (constraints, queries, query
  counts, atomicity) is practised without a server.
- The track teaches the current release and keeps a version note per area, because most codebases lag the
  current release by one or two upgrades.

## Sources

| Source | Used for | Why it is trusted |
| --- | --- | --- |
| Django documentation: tutorial, topic guides, how-to guides, deployment checklist, release notes | the whole track; version notes | the framework's own, versioned documentation |
| MDN, Django Web Framework (Python) module, and its example repository (CC0) | a second, independent walk through the basics, security and deployment | maintained by MDN, with working code |
| Django Girls tutorial | an optional gentle on-ramp | long-running, widely used beginner tutorial |
| Django REST framework documentation | REST APIs | the framework's own documentation and tutorial |
| HackSoft Django Styleguide (MIT) | project structure, services, selectors, errors, Celery usage | a widely used practitioner guide from a Django consultancy |
| Celery documentation, "First steps with Django" | background work | the project's own guide |
| Channels documentation and tutorial | real time | the project's own, under the Django organisation |
| CS50 Web Programming syllabus (Harvard) | order of topics: Django, models, testing, scalability, security | a university course; its lecture pages are keyword lists, used only for ordering |
| pytest-django documentation | testing with pytest | the plugin's own documentation |
