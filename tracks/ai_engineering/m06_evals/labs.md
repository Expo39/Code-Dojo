# Labs: m06_evals

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L6.1: A real evaluation run

- **Goal:** Build a golden set of 200 cases for your P1 or P2 project (including 20 you write from real failures), run it on three models with a code check and an LLM judge, and check the judge against your own labels on 30 outputs.
- **Services:** three models, a judge model
- **Estimated cost:** $5 to $15 (200 cases x 3 models x about 2,000 tokens, plus the judge's reading of each output)
- **Time:** about 6 hours
- **Done when:** a report: pass rate per model, judge agreement with you, cost per correct answer, and the three failure types that matter most
- **Teardown:** none

## L6.2: Evals in CI

- **Goal:** Run a cheap subset of the set in a CI pipeline on every prompt change and fail the build under a threshold; keep the full run for releases.
- **Services:** a CI service (a free tier is fine), a cheap model
- **Estimated cost:** $0 to $2 (30 cases per run)
- **Time:** about 3 hours
- **Done when:** a pull request that lowers the score and is blocked, and one that raises it and passes
- **Teardown:** none
