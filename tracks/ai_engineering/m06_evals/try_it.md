# Try it: m06_evals

Hands-on, 5 to 15 minutes each. Use any provider's free tier, a local model (for example Ollama) or a fake
model function, so nothing needs a GPU or a paid account unless a task says so. Done when the reading and recall
finish early; never instead of a discussion drill or an exercise. What you type goes in
`workspace/ai_engineering/m06_evals/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Error analysis** (`error_analysis`): Run a prompt on thirty inputs; read every output and write one failure label for each bad one; count and rank the labels.
- **Building a golden set** (`golden_sets`): Turn the ten worst inputs into a labelled set with expected properties (not exact text).
- **Graders: code checks and LLM judges** (`graders`): Write one code check and one LLM-judge rubric for the same property; compare both with your own judgement on ten outputs.
- **Regression evals in CI** (`regression_evals`): Put the set behind a pytest that fails when the pass rate drops below a threshold, using a fake model so it runs offline.
