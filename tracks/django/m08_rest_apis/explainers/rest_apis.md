# REST APIs: what makes an API RESTful, and the alternatives

*Reference explainer, checked against current documentation in November 2026. Frameworks and their defaults change: the tutor re-checks the live documentation before teaching from it.*

An **API** (application programming interface) is the set of requests one program can send to
another. A **web API** is one that is reached over HTTP: a browser, a mobile app or another server
sends a request to a URL and gets data back, usually as JSON (a plain-text format of keys and
values, `{"id": 3, "title": "Dune"}`).

**REST** (representational state transfer) is a style for designing web APIs, described by Roy
Fielding in 2000. An API is *RESTful* when it follows these rules:

1. **Resources are named by URLs.** The things the API manages are nouns in the URL:
   `/api/books/` is the collection of books, `/api/books/3/` is book 3. The URL never contains a
   verb such as `/getBook` or `/deleteBook`, because the verb is said by the HTTP method.
2. **Standard HTTP methods carry the action**, each with a fixed meaning: `GET` reads, `POST`
   creates, `PUT` replaces, `PATCH` changes part, `DELETE` removes. Because every client and
   server agrees on these meanings, tools such as caches and proxies can act on a request without
   knowing anything about the particular API.
3. **Status codes report the outcome**: 200 OK, 201 created, 204 deleted with nothing to return,
   400 invalid input, 401 not logged in, 403 not allowed, 404 not found, 500 a server crash.
4. **Stateless.** Every request carries everything the server needs, including who the caller is
   (a token or cookie). The server keeps no memory of earlier requests between them. Why: any
   server behind a load balancer can answer any request, so the service scales by adding servers.
5. **Cacheable.** Responses say whether they can be cached (`Cache-Control` headers), so a
   repeated `GET` can be answered by a cache instead of the server.
6. **Layered.** The client cannot tell whether it talks to the real server or to a proxy, cache
   or load balancer in between, so those can be added without changing the client.

**Idempotent** means that sending the same request twice leaves the server in the same state as
sending it once. `GET`, `PUT` and `DELETE` are idempotent; `POST` is not (two POSTs create two
books). Why it matters: a client whose request timed out can safely retry an idempotent request,
but retrying a POST can create a duplicate, which is why payment APIs ask for an *idempotency
key* on POST.

## The alternatives, and when each is chosen

- **GraphQL:** one endpoint; the client writes a query naming exactly the fields it wants, so a
  screen gets a book and its author's name in one request. Chosen for frontends with many
  different data needs. Costs: harder to cache (everything is a POST to one URL), and expensive
  queries need limits.
- **gRPC:** the client calls named functions defined in a `.proto` schema file; messages are
  compact binary (Protocol Buffers) over HTTP/2, with generated typed clients and streaming.
  Chosen for fast internal service-to-service calls. Cost: browsers cannot call it directly.
- **WebSockets:** a connection that stays open so the server can push data to the client at any
  time (a live dashboard, a chat). **Server-Sent Events** are the simpler one-way version over
  plain HTTP. REST, by contrast, only answers when asked, so live data over REST means polling.
- **Webhooks:** the reverse direction: instead of the client asking repeatedly "anything new?",
  the other service sends an HTTP POST to the client's URL when something happens (a payment
  succeeded, a ticket closed).
- **SOAP:** an older, XML-based style with strict contracts, still found in banking and
  government systems.
