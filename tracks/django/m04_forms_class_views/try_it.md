# Try it: m04_forms_class_views

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m04_forms_class_views/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Forms and validation** (`forms_validation`): Write a form with a cross-field rule (end date after start date) and show both field and form-level errors in the template.
- **POST, redirect, messages** (`post_redirect_get`): Build a create form that redirects on success with a message; reload the result page to prove the form is not resubmitted.
- **Generic views** (`generic_views`): Replace three function views with ListView, DetailView and CreateView; restrict the list to the current user's rows.
