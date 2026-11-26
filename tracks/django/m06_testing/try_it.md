# Try it: m06_testing

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m06_testing/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **TestCase and the test client** (`testcase_client`): Write a test for a view that checks status, content, a redirect after POST and the row it created.
- **pytest-django** (`pytest_django`): Convert one `TestCase` class to pytest-django functions with fixtures; compare lines and clarity.
- **Query-count tests** (`query_count_tests`): Add `django_assert_num_queries` to a list view, then add a new field that causes an N+1 and watch the test fail.
- **Isolation and slow things** (`test_isolation`): Write a test that needs real commits (on_commit); make it pass with `transaction=True` and explain why the default cannot.
