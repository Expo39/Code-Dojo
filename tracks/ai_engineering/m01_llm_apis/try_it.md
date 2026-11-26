# Try it: m01_llm_apis

Hands-on, 5 to 15 minutes each. Use any provider's free tier, a local model (for example Ollama) or a fake
model function, so nothing needs a GPU or a paid account unless a task says so. Done when the reading and recall
finish early; never instead of a discussion drill or an exercise. What you type goes in
`workspace/ai_engineering/m01_llm_apis/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **What a token is** (`theory_tokens`): Paste three texts (English prose, source code, a table of numbers) into a provider's tokeniser or token-counting call; compare tokens per character and say why they differ.
- **Calling a chat model API** (`chat_api_call`): Send one request with a system message and a user message to any provider (free tier) or to a local model in Ollama; print the answer, the finish reason and the usage numbers.
- **Context windows and context rot** (`context_window`): Send a prompt that is deliberately too long to a local model with a small window; note whether it errors or silently drops the start, and how you could have detected it.
- **Sampling and determinism** (`sampling_determinism`): Ask the same question five times at temperature 0 and five times at 1; compare the answers and say what you would use for extraction and for brainstorming.
- **API errors, rate limits and retries** (`api_errors_retries`): Write a small wrapper that retries a failing call (simulate failures with a fake function) with exponential backoff and jitter, and gives up after a cap.
