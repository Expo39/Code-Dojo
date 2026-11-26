# Try it: m05_auth_security

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m05_auth_security/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **A custom user model** (`user_model_custom`): Start a new project with a custom user model that logs in by email; create a superuser and log into the admin.
- **Permissions and groups** (`permissions`): Give one group the permission to change but not delete a model; log in as a member and check the admin and a protected view.
- **Web security basics** (`web_security`): Run `check --deploy` on your project and fix every warning you understand; write down the ones you will not fix and why.
- **Login limits and lockout** (`rate_limiting_lockout`): Add a counter that blocks the sixth failed login within a minute; test it, and write how an attacker could abuse it.
