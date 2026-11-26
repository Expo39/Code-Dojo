# Labs: m01_llm_apis

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L1.1: One request, four endpoints

- **Goal:** Call the same prompt through four routes: an OpenAI-compatible provider, a second provider's native SDK, a model on AWS through the Bedrock Converse API (using an IAM role or login, no keys in code), and a local model in Ollama.
- **Services:** provider accounts, Bedrock model access, a local runtime
- **Estimated cost:** $1 to $3 (a few thousand tokens per route; the lab is about learning the four request shapes, not spending)
- **Time:** about 3 hours
- **Done when:** a table of the four routes: request shape, how each reports tokens, latency, cost of the same prompt (computed with your m01 cost exercise and compared with the bill), and what you had to change to make one function call all four
- **Teardown:** nothing to tear down; remove unused model access and API keys you will not use again

## L1.2: Break it on purpose

- **Goal:** Trigger and handle every failure the API can give you: a bad key, a rate limit (by sending a burst), a too-long input, a timeout, an invalid parameter.
- **Services:** one provider, your retry wrapper from the try-it task
- **Estimated cost:** under $1 (a few hundred requests that mostly fail)
- **Time:** about 2 hours
- **Done when:** a test suite that proves each failure is classified as retryable or permanent and handled, with the wrapper's backoff visible in a log
- **Teardown:** none
