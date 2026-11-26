# Try it: m01_request_flow

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m01_request_flow/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Project and app layout** (`project_layout`): Create a project and an app from scratch with `startproject` and `startapp`; add the app to INSTALLED_APPS; draw what each generated file is for.
- **The request cycle** (`request_cycle`): Add a print or log line to a middleware, a view and a template tag; load a page and write the order of the lines you see.
- **Function views** (`function_views`): Write one view that returns HTML, one that returns JSON and one that redirects; test each with the Django test client.
- **Middleware** (`middleware`): Write a middleware that logs the method, path and time taken of every request, and move it up and down MIDDLEWARE to see what changes.
- **Templates** (`templates_basics`): Render a list of objects with a base template, a child template and a custom filter; print `<script>` as a value to see the escaping.
