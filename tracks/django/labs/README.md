# Labs: real accounts, real money

Module 12 has labs: you deploy a Django stack to a real cloud account and pay for it. A lab gives the goal, the
services, the cost and the "done when", never the steps. **Estimate each lab's cost first, run it, then compare
your estimate with the bill the next morning.**

## Set up once

1. A cloud account you can afford to make mistakes in (AWS is used here; Azure and Google Cloud have equivalents
   of every service named), never a company account.
2. Multi-factor authentication on the root user; then work with a limited login and roles, never root. No keys in
   code, files or screenshots.
3. A **budget with alerts** at 50%, 80% and 100% of a cap you choose, before anything else. Alerts do not stop
   spending and billing data lags by up to a day: they are a smoke detector, not a seatbelt.
4. Tag everything `lab=django` and the module. Describe the stack as code (Terraform, CloudFormation or the CDK)
   so that teardown is one command.

## Teardown, every lab, every time

Delete everything the same day; search by tag for leftovers (volumes, snapshots, load balancers, NAT gateways,
log groups, container images); read the bill and Cost Explorer the next morning, filtered by tag; write the real
cost next to your estimate. `dojo.py log lab <minutes> <id> --estimate E --cost C` records both.

## What a forgotten Django stack costs

The stack of lab 12.1 (web service, worker, Redis container, a small database, a load balancer) costs about
**$2.40 a day, about $17 a week, about $72 a month** if forgotten. These make it worse:

| Left running | Approximate cost | Notes |
| --- | --- | --- |
| A NAT gateway | $0.045 per hour plus $0.045 per GB, so about $32 a month idle | avoid it: use public subnets with tight security groups in labs |
| An application load balancer | $0.0225 per hour plus $0.008 per LCU-hour, about $0.73 a day with the minimum capacity unit | one per lab, deleted after |
| A small Fargate task (0.5 vCPU, 1 GB) | about $0.59 a day | $0.0405 per vCPU-hour and $0.0044 per GB-hour |
| A secret in the secrets service | $0.40 per month each | trivial but they accumulate |
| Logs | $0.50 per GB ingested | a debug logger in a loop can ingest gigabytes |
| A small managed database (`db.t4g.micro`) | about $0.016 per hour, plus storage and backups | the figure comes from third-party aggregators: confirm on AWS's page |

## Price sources (checked 26/11/2026; prices change: confirm on the calculator before you run)

| Price | How it was checked |
| --- | --- |
| Fargate, load balancer, Secrets Manager | read on AWS's own pricing pages (worked examples) |
| NAT gateway | AWS documentation example |
| Logs ($0.50 per GB ingested) | AWS's CloudWatch pricing page example; the rest of that page was not read in full |
| `db.t4g.micro` | third-party price aggregators agreeing with each other, not AWS's own page |

Total for the labs of this track, done as written and torn down the same day: roughly **$6 to $15**.
