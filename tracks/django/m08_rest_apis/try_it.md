# Try it: m08_rest_apis

Hands-on, 5 to 20 minutes each, on your own machine with a throwaway project (a virtual environment,
SQLite or a PostgreSQL container); nothing here costs money. Done when the reading and recall finish early;
never instead of a discussion drill or an exercise. What you type goes in
`workspace/django/m08_rest_apis/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Serializers** (`drf_serializers`): Write a ModelSerializer with a custom validation rule and a nested read-only field; try valid and invalid input in the shell.
- **API views, viewsets and routers** (`drf_views`): Build the same endpoint three ways (APIView, generic view, ViewSet with a router) and compare the code.
- **API authentication and permissions** (`api_authentication_permissions`): Protect an endpoint with token authentication and a custom permission; call it with and without a token using curl.
- **OpenAPI documentation** (`openapi_docs`): Generate the schema with drf-spectacular, serve the docs page and find one place where the generated schema is wrong.
