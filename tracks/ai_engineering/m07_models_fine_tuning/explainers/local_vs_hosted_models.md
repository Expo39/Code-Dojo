# Local versus hosted models

*Reference explainer, checked against current provider documentation in November 2026. Model names, limits and prices change quickly: the tutor re-checks the live documentation before teaching from it.*

## The two kinds of model

- A **hosted model** runs on a provider's servers and is reached through an API (OpenAI, Anthropic,
  Google, Mistral and others, or a cloud service such as Amazon Bedrock, Azure AI Foundry or Google
  Vertex AI that hosts several). It is usually the most capable, needs no hardware of your own, and you
  pay per token.
- A **local model** is an open-weight model (Llama, Qwen, Mistral, Gemma and others) that you run on your
  own machine or servers, through a runtime such as Ollama, llama.cpp or vLLM. A small one (1 to 8
  billion parameters, often **quantised**: stored with fewer bits per number to save memory) runs on a
  laptop or a small GPU. The data never leaves your machine and per-token cost is zero, but quality is
  lower on hard tasks and you operate it yourself.

## The trade-off

| | Hosted | Local or self-hosted |
| --- | --- | --- |
| Quality on hard tasks | highest | lower, closing for narrow tasks |
| Data leaves your control | yes (check retention and training terms) | no |
| Cost shape | per token, grows with use | fixed hardware and operations cost |
| Latency | network plus queueing | low on your own hardware, if it is big enough |
| Operations | none | updates, scaling, monitoring, GPUs |
| Availability and versions | provider can change or retire models | you pin the exact weights |

Open-weight does not always mean free to use commercially: read the licence.

## What goes in code, what goes to the model

A model is best at fuzzy work (understanding free text, classifying, summarising, drafting) and worst at
exact work (arithmetic, lookups, rules that must always hold). Put the exact parts in code and let the
model do the fuzzy parts. Smaller models need stricter, more spelled-out instructions, a few examples and
a strictly checked output.

## A common hybrid

Route by task: a small local model for redaction, classification and simple extraction; a hosted
frontier model for the hard cases. The router can be rules, a classifier or the small model's own
confidence. Measure before building a cascade: a stronger model at lower effort, a cache, or a shorter
prompt may remove the need.

## Trust and evaluation

A model writes confident "because" sentences even when it does not know the cause or the future, so
causes and forecasts need data from your own code, not the model's opinion. Whichever kind you choose,
decide with an evaluation set of your own cases, not with a public benchmark alone.

Check: a company wants to summarise customer emails that contain personal data. Which part could use a
hosted model, which must stay local, and what would you ask the provider before sending anything?
