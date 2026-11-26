# Try it: m08_cloud_deployment

Hands-on, 5 to 15 minutes each. Use any provider's free tier, a local model (for example Ollama) or a fake
model function, so nothing needs a GPU or a paid account unless a task says so. Done when the reading and recall
finish early; never instead of a discussion drill or an exercise. What you type goes in
`workspace/ai_engineering/m08_cloud_deployment/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Serving a model behind an API** (`api_service`): Wrap a model call (a fake one is fine) in a FastAPI endpoint with a validated request body and a streaming response; test it with curl.
- **Secrets, configuration and access control** (`secrets_config_iam`): Move a key from the source file to an environment variable and a `.env` file that is git-ignored; check with `git status` that it cannot be committed.
- **Containers for AI services** (`containers_for_ml`): Write a Dockerfile for that service with pinned dependencies; build it and run it with the key passed at run time.
- **Scaling and cloud cost** (`cloud_cost_scaling`): In a cloud account, set a budget alert at a small amount before anything else; write down the quotas and prices of one managed model service.
