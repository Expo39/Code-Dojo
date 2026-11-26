# Labs: m02_prompts_structured_output

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L2.1: Extract from 200 documents, three models

- **Goal:** Extract fields from 200 short real or synthetic documents (invoices, tickets, emails) into a schema with three models (a small, a mid-size, a reasoning model); validate with a schema library and retry on invalid output.
- **Services:** two or three hosted models (Bedrock and a provider), a schema library
- **Estimated cost:** $2 to $8 (200 requests x 3 models x about 1,500 input and 300 output tokens; the reasoning model costs most)
- **Time:** about 4 hours
- **Done when:** a results table (valid on first try, valid after retry, correct fields, tokens, cost, latency) and a choice of model you can defend with the numbers
- **Teardown:** none

## L2.2: Prompt injection of your own prompt

- **Goal:** Take the L2.1 prompt and try to make it ignore its instructions with ten adversarial documents; record what works.
- **Services:** the same models
- **Estimated cost:** under $1 (ten requests per model)
- **Time:** about 1 hour
- **Done when:** a list of attacks that worked and one change to the prompt or code that stops each
- **Teardown:** none
