# Projects

Exercises train single moves; projects put them together with nobody telling you the structure. Each
project has a goal, requirements and a "done when" list, but **no step-by-step guide**.

Rules:

- Write it yourself. The tutor answers questions, reviews your design and code (`review my project`) and
  gives hints, but writes none of it.
- Start with the smallest version that runs end to end, then add one feature at a time.
- Commit to git after every working step, in your own repository. Keys live in environment variables.
- Write tests for the core logic and an evaluation set for the model-dependent part.
- Log the time: `python dojo.py log project 60 P1 --note "added citations"`.

Code lives in `workspace/ai_engineering/projects/<name>/` (personal, gitignored) or in your own repository.

| # | Project | When | Skills |
| --- | --- | --- | --- |
| P1 | Questions over your own documents | after m04 | ingestion, chunking, embeddings, retrieval, citations, abstaining |
| P2 | A tool-using agent with limits and an evaluation set | after m06 | tool calling, the agent loop, step limits, golden set, regression eval |
| P3 | Capstone: ship an AI service | after m10 | API, container, keys, cost and latency logging, feedback, injection test |

## P1: Questions over your own documents

Goal: `python ask.py "question"` answers from a folder of documents you choose (notes, a manual, a public
FAQ) and shows which passages it used.

Requirements: ingestion that skips unchanged files; chunking you can justify; keyword and vector search
combined; an answer that cites passage ids; "not in the documents" when the passages do not answer; ten
labelled questions with the right passage for each.

Done when: you can say how often the right passage is in the top three, and which of your ten questions fail
for retrieval and which for generation.

## P2: A tool-using agent with limits and an evaluation set

Goal: an agent with three tools that solves tasks you define (for example a research assistant over a small
set of files), stopping safely.

Requirements: a step limit and a cost budget; every step logged; irreversible tools need approval in code; a
golden set of at least fifteen tasks with expected properties; a script that runs the set and fails below a
threshold, with a fake model so it runs offline.

Done when: you can compare two prompts or two models on the set, with cost and latency, and choose.

## P3: Capstone: ship an AI service

Goal: P1 or P2 as a service that someone else can call.

Requirements: a web API with validated requests and streamed answers; a Docker image with pinned dependencies
and no secrets in it; one JSON log line per request (model, tokens, latency, cost, prompt version, outcome)
with no raw personal data; a thumbs up or down stored with the prompt version; a prompt-injection test in
the evaluation set; a short README with the architecture, the cost per request and what you would do next.

Done when: a stranger can run it from the README, and you can say what it costs per thousand requests and how
you would know it had got worse.
