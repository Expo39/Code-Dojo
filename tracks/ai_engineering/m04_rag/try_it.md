# Try it: m04_rag

Hands-on, 5 to 15 minutes each. Use any provider's free tier, a local model (for example Ollama) or a fake
model function, so nothing needs a GPU or a paid account unless a task says so. Done when the reading and recall
finish early; never instead of a discussion drill or an exercise. What you type goes in
`workspace/ai_engineering/m04_rag/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **The RAG pipeline** (`rag_pipeline`): Build a 50-line RAG over ten text files: chunk, embed, retrieve the top three, assemble the prompt, call a model; answer three questions.
- **Citations and grounded answers** (`citations_grounding`): Change the prompt so each claim carries a passage id and the model says "not in the documents" when it must; test with one unanswerable question.
- **Debugging RAG** (`rag_failures`): Write five questions with the right passage id for each; measure how often the right passage is in the top three, before looking at any generated answer.
