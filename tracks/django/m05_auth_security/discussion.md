# Discussion questions: m05_auth_security

Questions for a discussion drill: answer out loud, at your level, with a concrete
example; the tutor follows up (why? when would you not?) and judges against the read-first sources (track
README). No answers here on purpose.

1. Why decide on a custom user model before the first migration?
2. What is the difference between authentication and authorisation? Give a Django example of each.
3. How do Django's templates and ORM protect against XSS and SQL injection, and how can you still get it wrong?
4. What are the trade-offs between database, cache and signed-cookie sessions?
5. How would you stop password guessing without letting an attacker lock out a real user?
6. What does `manage.py check --deploy` look for, and which of its warnings would you never ignore?
7. How does a read-only service account differ from a normal user, and where would you enforce it?
