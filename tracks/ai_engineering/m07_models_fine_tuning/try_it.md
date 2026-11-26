# Try it: m07_models_fine_tuning

Hands-on, 5 to 15 minutes each. Use any provider's free tier, a local model (for example Ollama) or a fake
model function, so nothing needs a GPU or a paid account unless a task says so. Done when the reading and recall
finish early; never instead of a discussion drill or an exercise. What you type goes in
`workspace/ai_engineering/m07_models_fine_tuning/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **The model landscape and choosing a model** (`model_landscape`): Pick three models (one closed, two open); read their model cards and fill a table of context length, licence, price or hardware, and strengths.
- **Quantisation and local inference** (`quantisation_local_inference`): Run a small quantised model locally; measure tokens per second and memory; repeat with a different quantisation and compare.
- **Fine-tune or not** (`fine_tune_or_not`): For three tasks of your choice, write which of prompting, RAG and fine-tuning you would try first and the one measurement that would change your mind.
- **Dataset engineering and synthetic data** (`synthetic_data`): Generate fifty synthetic support tickets with a model, sample ten, and write down every flaw you find before deciding whether to use them.
