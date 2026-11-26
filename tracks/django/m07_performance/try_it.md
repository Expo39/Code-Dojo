# Try it: m07_performance

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m07_performance/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **The N+1 problem** (`n_plus_one`): Load a list page with the debug toolbar, count the queries, fix the N+1 with `select_related` and `prefetch_related`, and measure again.
- **Database indexes** (`db_indexes`): Seed 100,000 rows; time a filter before and after adding an index; read `EXPLAIN` for both.
- **Caching** (`caching_layers`): Cache an expensive aggregate in Redis with a 60-second timeout and invalidate it when a row changes.
- **Precomputed rollups** (`rollup_tables`): Build a daily summary table from raw rows with a management command; compare its answer with the raw aggregate.
