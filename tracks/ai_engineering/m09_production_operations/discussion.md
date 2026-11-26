# Discussion questions: m09_production_operations

Questions for a discussion drill: answer out loud, at your level, with a concrete
example; the tutor follows up (why? when would you not?) and judges against the read-first sources (track
README). No answers here on purpose.

1. How do you make a model call reliable in production: timeouts, retries, fallbacks, budgets?
2. What would you log, trace and monitor for an LLM feature? What must you not log?
3. Explain prompt caching. What silently breaks a cache?
4. A team's model bill doubled. Walk through the levers you would try, in order.
5. How do you reduce latency, and which lever do you try first?
6. Before building a cheap-model-first cascade, what simpler option would you measure first?
7. How do you know a prompt change made things better, not just different?
8. Draw the components around a model in a production app and say what each one is for.
9. How do you collect user feedback and turn it into something that improves the system?
10. What needs scheduling in an AI application, and what happens when a run fails?
