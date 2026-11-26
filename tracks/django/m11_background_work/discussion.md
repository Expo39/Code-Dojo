# Discussion questions: m11_background_work

Questions for a discussion drill: answer out loud, at your level, with a concrete
example; the tutor follows up (why? when would you not?) and judges against the read-first sources (track
README). No answers here on purpose.

1. Which work belongs in a background task, and which should stay in the request?
2. A task is queued, then the transaction rolls back. What goes wrong, and how do you prevent it?
3. What does it mean for a task to be idempotent, and how do you make one so?
4. Why might a message carry only an id and not the data?
5. What can go wrong with scheduled tasks and time zones or daylight saving?
6. What do prefetch and a memory limit on a worker protect against?
7. How do Django's built-in Tasks differ from Celery, and when would you pick each?
