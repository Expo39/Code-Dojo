# Try it: m11_background_work

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m11_background_work/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Celery tasks with Django** (`celery_tasks`): Run Redis in Docker, start a worker, and call a task that sleeps; watch the worker log.
- **Retries and idempotency** (`task_reliability`): Make a task fail twice then succeed with retries and backoff; run it twice and prove the second run changes nothing.
- **Enqueue after commit** (`on_commit_tasks`): Queue a task inside a transaction that then fails; fix it with `on_commit` and show the difference.
- **Scheduled tasks** (`beat_scheduling`): Schedule a task every minute with the database scheduler; change its schedule from the admin.
