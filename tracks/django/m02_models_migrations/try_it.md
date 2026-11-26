# Try it: m02_models_migrations

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m02_models_migrations/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Models and fields** (`model_fields`): Define a model with a unique field, a check constraint and default ordering; run `sqlmigrate` and read the SQL it produces.
- **Relationships** (`relations`): Model authors, books and genres (one-to-many and many-to-many); change `on_delete` and see what deleting an author does in each case.
- **The migration workflow** (`migrations_workflow`): Create two migrations on two branches on purpose, merge them, and resolve the conflict with `makemigrations --merge`.
- **Data migrations** (`data_migrations`): Write a reversible `RunPython` migration that fills a new column from an old one; run it forwards and backwards.
- **The admin site** (`admin_site`): Register your models with `list_display`, `search_fields`, a filter and an inline; add a custom admin action.
