# Try it: m10_async_realtime

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m10_async_realtime/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Async views and the async ORM** (`async_views`): Write an async view that calls two slow outside services at once with `asyncio.gather`; compare the time with a sync version.
- **Channels consumers and routing** (`channels_consumers`): Follow the Channels chat tutorial to a working room; write what each file is for.
- **Channel layers** (`channel_layers`): Send a group message from a normal view and see it arrive in an open browser tab.
- **WebSocket authentication** (`websocket_auth`): Reject an anonymous WebSocket connection and one from a wrong origin; test both.
