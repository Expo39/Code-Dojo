# Discussion questions: m10_async_realtime

Questions for a discussion drill: answer out loud, at your level, with a concrete
example; the tutor follows up (why? when would you not?) and judges against the read-first sources (track
README). No answers here on purpose.

1. What does ASGI add to WSGI, and what runs differently in production?
2. When does an async view help, and when does it only add complexity?
3. What happens if you call the synchronous ORM inside an async view?
4. How does a Channels group deliver one message to many connected users, and what does the channel layer do?
5. How do you authenticate a WebSocket connection, and what can an attacker do with a missing origin check?
6. Polling, server-sent events or WebSockets for a live dashboard: how do you choose?
