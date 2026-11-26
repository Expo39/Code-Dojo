# Labs: real accounts, real services, real money

Exercises teach the engineering offline with fake models. **Labs are the other half: you do the work on real
services with your own accounts, and you pay for it.** Each module has a `labs.md` with tasks, what they cost,
and how to tear them down. A lab gives the goal, the services, the cost, and "done when": never the steps.
Reading the provider's documentation to find them is the skill.

Cost is part of the lesson. Before each lab, estimate its cost yourself (module 1's cost exercise is the
method), run it, then compare your estimate with the bill the next day.

## Set up once (lab 0)

1. **A cloud account you can afford to make mistakes in**: AWS is used in the labs (Azure and Google Cloud have
   equivalents of every service named; do the managed-service lab of module 8 on a second cloud after the first).
   Use a separate account or a clearly tagged set of resources, never a company account.
2. **Secure it first**: multi-factor authentication on the root user, then stop using root. Create a user or an
   identity-centre login with only the permissions a lab needs, and use roles for services. No access keys in
   code, files or screenshots.
3. **Budget and alerts before anything else**: a monthly budget with alerts at 50%, 80% and 100% of a cap you
   choose, plus anomaly detection. **Alerts do not stop spending, and billing data lags by up to a day**, so
   they are a smoke detector, not a seatbelt. Your real protection is the teardown routine below.
4. **Tag everything** `lab=ai-eng` and the module, so Cost Explorer and a tag search can show everything a lab
   created.
5. **Infrastructure as code** for any lab with more than two resources (Terraform, CloudFormation or the CDK):
   teardown is one command, and writing it is itself practical engineering.
6. **Provider accounts**: one or two model providers (an OpenAI-compatible API, and one more) with a prepaid
   balance of a few dollars and a spending limit set in their console.

## The teardown routine (every lab, every time)

1. Delete the lab's resources the same day (`terraform destroy`, or delete the stack).
2. Search by tag for anything left (Resource Groups tag search), and check by hand the usual leftovers:
   volumes, snapshots, load balancers, NAT gateways, elastic IPs, log groups, vector collections, ECR images.
3. Check Billing and Cost Explorer **the next morning**, filtered by tag, and write down the real cost beside
   your estimate in your lab log.

## Money traps (what a forgotten lab costs)

| Left running | Approximate cost | Notes |
| --- | --- | --- |
| A GPU instance (`g5.xlarge`, `g6.xlarge`) | about $0.80 to $1.00 per hour, so **$19 to $24 per day** | stop is not delete: its disk keeps billing |
| OpenSearch Serverless collection (the default vector store when a managed knowledge base is created with the quick-create option) | **about $175 to $350 per month at the classic minimum** ($0.24 per OCU-hour; 2 OCUs minimum, 0.5 plus 0.5 for a dev-test collection) | deleting the knowledge base may leave the collection billing; delete it separately. The newer collection type is reported to have no minimum: check the current page |
| NAT gateway | about $0.045 per hour plus $0.045 per GB, so **about $32 per month** idle | avoid it in labs: put tasks in public subnets with tight security groups |
| Application load balancer | $0.0225 per hour plus $0.008 per LCU-hour, so about $16 per month idle | one per lab, deleted after |
| A small Fargate task (0.5 vCPU, 1 GB) | about $0.59 per day | $0.0405 per vCPU-hour and $0.0044 per GB-hour |
| A secret in the secrets service | $0.40 per month each | trivial, but they accumulate |
| Logs | $0.50 per GB ingested | a chatty debug logger can ingest gigabytes |

## Price sources (checked 26/11/2026; prices change: confirm on the calculator before you run)

| Price | Value | How it was checked |
| --- | --- | --- |
| Fargate vCPU and memory (us-east-1) | $0.000011244 per vCPU-second, $0.000001235 per GB-second | AWS pricing page worked example |
| Application load balancer (us-east-1) | $0.0225 per hour, $0.008 per LCU-hour | AWS pricing page worked examples |
| Secrets Manager | $0.40 per secret per month, $0.05 per 10,000 calls | AWS pricing page worked example (region not stated) |
| OpenSearch Serverless | $0.24 per OCU-hour (indexing and search), classic minimum 2 OCUs (0.5 plus 0.5 dev-test) | AWS pricing page worked examples; the page's own examples do not all add up, so treat as indicative |
| S3 Vectors | $0.06 per GB-month stored, $0.20 per GB uploaded, $2.50 per million queries plus a small per-TB charge | AWS pricing page worked examples |
| NAT gateway | $0.045 per hour, $0.045 per GB processed | AWS documentation example |
| Bedrock small model example | $0.04 and $0.08 per million input and output tokens (a 4-billion-parameter open model) | AWS pricing page table row |
| `g5.xlarge`, `g6.xlarge` on demand (us-east-1) | $1.006 and $0.8048 per hour; spot about $0.42 to $0.74 for `g6` | third-party price aggregators agreeing with each other, not AWS's own page |
| `db.t4g.micro` | about $0.016 per hour | third-party aggregators |
| Guardrails | $0.15 per 1,000 text units for content filters | an AWS announcement; the pricing page itself was not confirmed |
| Larger hosted models | check the provider's page; mid-size models have been around single-digit dollars per million input tokens and low double digits per million output tokens | not verified: always read the live page |

## Estimated cost of the whole track

Done as written, with every lab torn down the same day, roughly **$35 to $115 in total** across the ten
modules (the GPU labs in module 7 and 8 and the evaluation runs in module 6 are most of it). The same labs
with a forgotten GPU instance, vector collection or NAT gateway can cost that much again **per month**. Learn
the teardown before the first expensive lab, not after.
