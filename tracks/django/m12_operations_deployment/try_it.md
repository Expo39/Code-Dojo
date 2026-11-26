# Try it: m12_operations_deployment

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m12_operations_deployment/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **A Compose stack** (`compose_stack`): Write a Compose file for web, worker, PostgreSQL and Redis; bring it up from empty volumes and open the site.
- **Reverse proxy and HTTPS** (`reverse_proxy_https`): Put Caddy or nginx in front with a local certificate; check that Django generates https URLs and that cookies are secure.
- **Migrations in a release** (`release_migrations`): Split a column rename into three safe releases and write what each release does.
- **Backup and restore** (`backup_restore`): Back up the database, delete it, restore it, and compare row counts.
- **Upgrading Django** (`version_upgrades`): Run your tests with `-W error::DeprecationWarning` and write a list of what the next Django version will break.
