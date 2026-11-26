# Labs: m08_cloud_deployment

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L8.1: Ship your service to the cloud, then remove it

- **Goal:** Package the P1 or P2 service in a container, push it to a registry, run it on a managed container service behind a load balancer, keep its model key out of the image (a secrets service or a role), put a budget alarm on the account, and call it from your laptop.
- **Services:** a registry, ECS Fargate (about $0.59 per day), an application load balancer (about $0.73 per day), a secret ($0.40 per month), a log group
- **Estimated cost:** $2 to $4 if deleted the same day; about $10 per week if forgotten (Fargate plus load balancer is roughly $1.30 per day)
- **Time:** about 6 hours
- **Done when:** a public URL that answers with streaming, no secret in the image (prove it by inspecting the image), and the real cost of the day
- **Teardown:** delete everything with one command from your infrastructure code, then check by tag and in the billing console the next morning

## L8.2: The same API in front of a GPU model

- **Goal:** Route the service's requests to the open model you served in L7.1 behind the same API, with an automatic fall-back to a hosted model when the GPU instance is down.
- **Services:** one GPU instance for a few hours, the L8.1 service
- **Estimated cost:** $4 to $12 (GPU hours at about $0.80 to $1.00 each)
- **Time:** about 5 hours
- **Done when:** a failover test: stop the GPU instance mid-load and show the service keep answering through the fall-back, with the extra latency measured
- **Teardown:** terminate the GPU instance and delete its volume; delete the service

## L8.3: The teardown audit

- **Goal:** Without looking at your own notes, list every resource that still exists in the account from this module's labs using tags and the billing console, and delete what is left.
- **Services:** Resource Groups tag search, Cost Explorer
- **Estimated cost:** $0 (reading only)
- **Time:** about 1 hour
- **Done when:** an empty tag search and a flat cost line the next day
- **Teardown:** this is the teardown
