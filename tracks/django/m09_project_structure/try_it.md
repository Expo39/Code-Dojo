# Try it: m09_project_structure

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m09_project_structure/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Services and selectors** (`services_selectors`): Refactor one fat view into a service function and a selector; check the view is now only HTTP.
- **Managers and custom QuerySets** (`managers_querysets`): Turn three repeated filters into QuerySet methods and chain them in a view.
- **Management commands** (`management_commands`): Write a management command that is safe to run twice, with a `--dry-run` option.
- **Feature flags** (`feature_flags`): Add a flag that shows a new page to 10% of users; remove it and the dead code afterwards.
