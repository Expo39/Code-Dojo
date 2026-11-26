# Discussion questions: m02_models_migrations

Questions for a discussion drill: answer out loud, at your level, with a concrete
example; the tutor follows up (why? when would you not?) and judges against the read-first sources (track
README). No answers here on purpose.

1. What does a migration file contain, and why does Django keep them in version control?
2. Two developers each create a migration on separate branches. What happens when the branches merge, and how do you fix it?
3. What does `on_delete` decide, and how do you choose between CASCADE, PROTECT and SET_NULL?
4. How would you rename a column on a large table with no downtime?
5. Why must a data migration use `apps.get_model` instead of importing your model?
6. When is a database constraint better than validation in Python, and why have both?
7. What is the admin good for, and when would you build your own screens instead?
