# Try it: m09_production_operations

Hands-on, 5 to 15 minutes each. Use any provider's free tier, a local model (for example Ollama) or a fake
model function, so nothing needs a GPU or a paid account unless a task says so. Done when the reading and recall
finish early; never instead of a discussion drill or an exercise. What you type goes in
`workspace/ai_engineering/m09_production_operations/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Reliability: timeouts, fallbacks and budgets** (`reliability`): Add a timeout, one retry and a fallback to a second (fake) model to a call wrapper; write a test for each path.
- **Caching: prompt, response and semantic** (`caching`): Cache responses for identical requests in a dict; measure the hit rate on a repeated list of questions; note what a near-duplicate question does.
- **Observability for LLM features** (`observability`): Log one JSON line per call (model, tokens, latency, cost, prompt version, outcome) with no raw personal data; compute the average cost per request from the log.
- **Architecture of a production AI application** (`ai_architecture`): Sketch the architecture of a support chatbot with a gateway, a router, retrieval, guardrails and a cache; mark where each failure you know about would be caught.
- **User feedback and UX for AI** (`user_feedback`): Add a thumbs up or down and a free-text field to a toy app and store each with the prompt version; write the query that finds the worst prompts.
