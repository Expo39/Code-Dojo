# AI engineering track

Last reviewed: 26 November 2026, against current provider documentation (OpenAI, Anthropic and Google APIs,
Amazon Bedrock, Azure AI Foundry, Google Vertex AI), Python 3.10 or newer, and the curricula under "Sources".
Builds on the Python track.

How to build products on top of foundation models: the work of an **AI engineer**. Call a model through an
API, shape its output, give it your data (embeddings, search, RAG), let it use tools (agents, MCP), measure
it (evals), choose and adapt models (open-weight, fine-tuning), put it in the cloud, run it in production
(reliability, caching, observability, cost) and keep it safe. Every module is vendor-neutral: examples use
several providers, a cloud's managed service, and local open models. One of the tracks a learner can choose;
nothing here is compulsory.

Not covered, on purpose: training a model from scratch and the mathematics behind it (the "LLM scientist"
side), research on image and video models, low-code builders, and using AI tools to write or review code
(that is part of ordinary engineering practice, in the Python track and its reading and debugging work).

## Prerequisites

Python fluency: functions, dicts, exceptions, JSON, modules, a little `pytest` (the first milestone of the
Python track). The command line and basic Docker help from module 8 on. No GPU is needed anywhere, and no
machine-learning background: the theory lines below explain what each module needs.

## How lessons work in this track

Most concepts start from a **source you read yourself**, then a recall, then questions, then a small build:

1. **Read** the source named under "Read first" (one stretch at a time).
2. **Recall**: close it and say, in your own words, the three to five points that matter, one concrete
   example and one thing you would push back on.
3. **Questions**: the module's `discussion.md`, answered out loud; the tutor follows up (why? when would you
   not?) and scores the answer. A gap gets one short explanation.
4. **Build it**: a short exercise (module 1 and 2 have them) or the matching `try_it.md` task.
5. **Revise** from the module's `explainers/`, the reference notes for the topics learners ask about most.

`teach me <topic>` (PRIMM) is used where code behaviour is the point. Each block stays inside its own steps
(`docs/CHECKLISTS.md`, section 8); anything else that comes up is noted and offered afterwards.

## Hands-on setup

Exercises use deterministic fake models, so they run offline and cost nothing. For real calls use any
provider's free tier or a few euros of credit, or a local model (for example Ollama on CPU with a small
quantised model). For cloud tasks, **set a budget alert first**, use the free tier, and delete what you
create. Keep keys in environment variables, never in code.

## Modules

| Module | Focus | Status |
| --- | --- | --- |
| m01_llm_apis | the AI engineering stack, how models are built, tokens, calling a chat API, the context window, sampling, cost and latency, errors and retries | seeded |
| m02_prompts_structured_output | prompt structure, few-shot, reasoning prompts, multimodal inputs, structured output and validation, hallucination and grounding | seeded |
| m03_embeddings_search | embeddings, similarity search, chunking, ingestion pipelines, keyword search and BM25, vector databases, hybrid search and reranking | planned |
| m04_rag | the RAG pipeline, citations and abstaining, debugging a wrong answer, RAG against long context | planned |
| m05_tools_agents | tool calling, workflows against agents, the agent loop, planning, tool design, MCP, agentic RAG, context engineering and memory, multi-agent systems, frameworks | planned |
| m06_evals | error analysis, golden sets, code and LLM-judge graders, regression evals, evaluating RAG and agents, judging a new model | planned |
| m07_models_fine_tuning | choosing models, local and hosted, quantisation, fine-tune or not, dataset engineering, LoRA | planned |
| m08_cloud_deployment | serving behind an API, secrets and access, containers, managed cloud model services, serving open models on GPUs, inference optimisation, scaling and cost | planned |
| m09_production_operations | reliability, caching, latency, observability, cost control, architecture of a production AI app, user feedback, orchestration | planned |
| m10_safety_security | prompt injection, excessive agency, guardrails, sensitive data, tool-server security, responsible AI, regulation basics | planned |

Modules marked planned have their concepts, lesson topics, discussion questions and try-it tasks; their
exercises are written when a learner reaches them (`dojo-new-exercise`). Projects are in `projects/`.

## Read first, per module

- **m01**: Chip Huyen, *AI Engineering*, ch. 1 and 2 (the stack, foundation models, sampling, structured
  outputs); a provider's chat API reference and tokeniser or token-counting page; the Hugging Face Agents course,
  unit 1 ("What are LLMs?", "Messages and special tokens").
- **m02**: *AI Engineering*, ch. 5 (prompt engineering, including defensive prompting); a provider's prompt-writing
  and structured-output guides; Microsoft *Generative AI for Beginners*, lessons 4 and 5.
- **m03**: LLM Zoomcamp, module 2 (vector search); *Generative AI for Beginners*, lesson 8; the embeddings and
  vector-store pages of the AI Engineer roadmap.
- **m04**: LLM Zoomcamp, module 1 part 1 (a RAG pipeline from scratch) and module 6 (hybrid search, reranking);
  *AI Engineering*, ch. 6, the RAG part; *Generative AI for Beginners*, lesson 15.
- **m05**: LLM Zoomcamp, module 1 part 2 (function calling, the agentic loop); Hugging Face Agents course, units 1
  to 3; Microsoft *AI Agents for Beginners* (tool use, agentic RAG, planning, multi-agent, protocols, context
  engineering, memory); the Model Context Protocol documentation and the Hugging Face MCP course.
- **m06**: *AI Engineering*, ch. 3 and 4; LLM Zoomcamp, module 4; Hamel Husain and Shreya Shankar's free evals
  course; the documentation of an evaluation library (for example DeepEval or Ragas).
- **m07**: *AI Engineering*, ch. 7 and 8; *Generative AI for Beginners*, lessons 16, 18 and 19; the "Running LLMs"
  and "Quantization" parts of the LLM course roadmap; the Hugging Face PEFT and Ollama documentation.
- **m08**: *AI Engineering*, ch. 9; the "Deploying LLMs" and "Inference optimization" parts of the LLM course
  roadmap; the user guides of Amazon Bedrock, Azure AI Foundry and Google Vertex AI; vLLM, FastAPI and Docker
  documentation.
- **m09**: *AI Engineering*, ch. 10; LLM Zoomcamp, modules 3 and 5; *Generative AI for Beginners*, lessons 12
  and 14; the OpenTelemetry GenAI conventions and the docs of a tracing tool (for example Langfuse).
- **m10**: OWASP Top 10 for LLM Applications; *Generative AI for Beginners*, lessons 3 and 13; Microsoft *AI Agents
  for Beginners*, "Securing AI agents"; the EU AI Act transparency obligations.

## Theory (offered just in time, per module)

- m01: what a token is; what pre-training and post-training do; why everything is counted in tokens.
- m03: what an embedding is (a list of numbers whose distance means similarity).
- m06: why "it looked fine on a few examples" is not an evaluation.

## Bar

Able to build, in Python and with no framework, a small service that answers questions over its own documents
with citations, uses a tool in a loop with limits, is covered by a regression evaluation set, runs in a
container behind an API with its keys outside the code, logs cost and latency per request, and resists a
simple prompt-injection test; and to explain each choice (when not to use RAG, an agent or fine-tuning, which
provider or model, local or hosted) with a measurement or a trade-off.

## Left out, and why

- Training from scratch, the maths of neural networks, pre-training data pipelines: a different job (the
  "LLM scientist" path in the sources); module 1's theory lines give the picture an AI engineer needs.
- Image and video generation beyond calling an API (module 2): a specialist area.
- Low-code AI builders: no transferable engineering skill beyond the concepts already here.
- A single vendor's coding assistant and its configuration: it is a tool for developers, not part of building
  AI products.

## Where this track departs from its sources

- The sources need API keys or credits from lesson one; here the exercises use fake models first, so every
  learner can practise the engineering (parsing, retries, cost, evaluation) offline.
- The sources scatter cloud and deployment; here they are one module, with a budget alert first.
- Evaluation is taught early as a habit (error analysis in module 2's try-it tasks) as well as in its own
  module, because the sources that put it last show learners building without a way to tell better from worse.
- Reading a source is followed by recall and spoken questions, not only by a quiz.

## Sources

| Source | Used for | Why it is trusted |
| --- | --- | --- |
| Chip Huyen, *AI Engineering* (O'Reilly, 2025) and its public chapter summaries | the overall shape: stack, models, evaluation, prompting, RAG and agents, fine-tuning, datasets, inference, architecture | the standard practitioner book; ten chapters that every other source maps onto |
| DataTalksClub LLM Zoomcamp | RAG from scratch, vector search, orchestration, evaluation, monitoring, hybrid search, capstone | free, maintained, hands-on; builds with plain Python first |
| Microsoft *Generative AI for Beginners* and *AI Agents for Beginners* (MIT) | lesson order, responsible AI, UX, lifecycle, agent patterns | maintained lesson-by-lesson courses with code |
| Hugging Face Agents course and MCP course (Apache-2.0) | agents, frameworks, MCP | free, maintained, by the model hub's maintainers |
| The AI Engineer roadmap (roadmap.sh) and the LLM course roadmap | a coverage check of topics | community maps, used only to find gaps, never as a syllabus |
| Provider and cloud documentation (OpenAI, Anthropic, Google, Amazon, Microsoft) | exact API behaviour, quotas, prices | the vendors' own, current pages: checked live before teaching |
| Hamel Husain and Shreya Shankar, evals course; OWASP Top 10 for LLM Applications | evals, security | leading practitioner and standards-body material |
