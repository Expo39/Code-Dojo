# Try it: m02_prompts_structured_output

Hands-on, 5 to 15 minutes each. Use any provider's free tier, a local model (for example Ollama) or a fake
model function, so nothing needs a GPU or a paid account unless a task says so. Done when the reading and recall
finish early; never instead of a discussion drill or an exercise. What you type goes in
`workspace/ai_engineering/m02_prompts_structured_output/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Structuring a prompt** (`prompt_structure`): Take one vague prompt ("summarise this") and rewrite it with a role, task, constraints, input delimiters and an output format; run both five times and compare how stable the outputs are.
- **Few-shot examples** (`few_shot_prompting`): Build a five-category ticket classifier with and without three examples; score both on ten labelled inputs that are not the examples.
- **Validating model output with a schema** (`schema_validation`): Define a Pydantic model (or JSON Schema) for a recipe; validate three model outputs against it, one of them invalid, and print a retry message that names the failing field.
- **Hallucination and grounding** (`hallucination`): Ask a model about a made-up library function; then give it the real documentation and a rule to answer only from it; compare the two answers.
- **Reasoning prompts and test-time compute** (`reasoning_cot`): Ask a multi-step arithmetic question with and without "think step by step" (or a reasoning model); compare accuracy, tokens and latency over ten questions.
- **Multimodal inputs and outputs** (`multimodal_inputs`): Send a photo of a receipt to a vision-capable model and extract the total as JSON; try a blurry version and note what breaks.
