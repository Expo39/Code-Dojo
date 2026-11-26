# Labs: m10_safety_security

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L10.1: Red-team your own RAG and agent

- **Goal:** Write 30 attacks (injected instructions in documents, data exfiltration through a tool, a request that needs a human) and run them against P1 and P2; add one control in code and, if you want, a managed guardrail service; run again.
- **Services:** your projects, optionally a managed guardrail (about $0.15 per 1,000 text units for content filters)
- **Estimated cost:** $1 to $4 (30 attacks x a few runs and guardrail text units)
- **Time:** about 5 hours
- **Done when:** a table of attacks, which succeeded before and after, and which controls were in code rather than in the prompt
- **Teardown:** remove any guardrail you created

## L10.2: Least privilege audit

- **Goal:** Take the role of every service you built and remove permissions one by one until it fails; keep the smallest set; write down what a leaked key could do before and after.
- **Services:** IAM, the access analyser
- **Estimated cost:** $0 (no running resources needed)
- **Time:** about 3 hours
- **Done when:** a before and after list of permissions per role, and the blast radius of each leaked credential
- **Teardown:** none
