# Discussion questions: m03_orm_queries

Questions for a discussion drill: answer out loud, at your level, with a concrete
example; the tutor follows up (why? when would you not?) and judges against the read-first sources (track
README). No answers here on purpose.

1. When does a QuerySet actually run a query? Give three operations that evaluate it and three that do not.
2. What is the difference between `filter()` chained across a multi-valued relation and one `filter()` with two conditions?
3. When do you use an F expression instead of reading a value, changing it and saving?
4. What does `bulk_update` skip that `save()` does, and when is that a problem?
5. Two requests try to spend the same balance at the same time. What goes wrong and how do you prevent it?
6. What does `transaction.on_commit` do, and why would you enqueue a background task from it?
7. When is raw SQL justified, and how do you keep it safe?
