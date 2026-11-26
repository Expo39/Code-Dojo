# Try it: m03_orm_queries

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m03_orm_queries/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **QuerySets** (`queryset_basics`): In the shell, build a queryset and print `connection.queries` after each step to see exactly when the database is hit.
- **Lookups, Q and F** (`lookups_q_f`): Write the same filter with chained filters and with one filter across a many-to-many relation; compare the SQL.
- **Aggregation** (`aggregation`): Compute the average, total and count per group with `values().annotate()`; then filter on the annotation.
- **Transactions and locking** (`transactions_locking`): Run two shell sessions that both try to take money from one row inside `select_for_update` (use PostgreSQL); watch the second wait.
- **Raw SQL and EXPLAIN** (`raw_sql_fallback`): Run `explain()` on a slow-looking queryset, add an index, and compare the plans.
