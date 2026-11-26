# Labs: m09_production_operations

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L9.1: Observe 1,000 requests

- **Goal:** Send 1,000 realistic requests through your deployed service; emit one structured log line each (model, tokens, latency, cost, prompt version, outcome) with no personal data, plus traces in an open-source or hosted tracing tool; build the dashboard that shows cost per request and the slowest 1%.
- **Services:** your service, a log service ($0.50 per GB ingested), a tracing tool (a free tier or self-hosted)
- **Estimated cost:** $2 to $8 (model tokens for 1,000 requests plus logs; keep logs small)
- **Time:** about 5 hours
- **Done when:** a dashboard and the answer to "which 10 requests cost the most and why?"
- **Teardown:** delete log groups and the tracing deployment

## L9.2: Caching and cost drills

- **Goal:** Measure what prompt caching, an exact-match response cache and a smaller model for easy cases each save on the same 1,000 requests, and what each does to quality on your golden set.
- **Services:** the L9.1 setup
- **Estimated cost:** $1 to $4 (repeat runs of the same request set)
- **Time:** about 4 hours
- **Done when:** a table of saving against quality loss, and the one change you would ship first
- **Teardown:** none

## L9.3: Game day

- **Goal:** Break your own system on purpose: make the provider return errors, slow down, return garbage JSON, and exhaust your token budget; fix what fails.
- **Services:** your service with a fake provider switch
- **Estimated cost:** $0 to $2 (mostly a fake provider)
- **Time:** about 3 hours
- **Done when:** a runbook with each failure, how you detected it, and the alarm that would have told you
- **Teardown:** none
