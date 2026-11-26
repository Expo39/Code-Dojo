# Discussion questions: m04_forms_class_views

Questions for a discussion drill: answer out loud, at your level, with a concrete
example; the tutor follows up (why? when would you not?) and judges against the read-first sources (track
README). No answers here on purpose.

1. Why redirect after a successful POST instead of rendering the page?
2. What does the CSRF token protect against, and what happens if you disable the check on a form?
3. Where does validation belong: the form, the model, the database, or all three?
4. When is a function view better than a class-based view, and the other way round?
5. A generic view shows every row. How do you restrict it to what the current user may see?
6. How does `ModelForm.save(commit=False)` help, and what must you remember to do next?
