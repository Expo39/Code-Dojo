# Labs: m05_tools_agents

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L5.1: An agent whose tools are serverless functions

- **Goal:** Build an agent loop (your code, a model's tool calling) with three tools that are small cloud functions (for example a lookup, a calculation and a write that needs approval); add a step limit and a cost budget; log every step.
- **Services:** a model with tool calling, three serverless functions, one IAM role per function with least privilege
- **Estimated cost:** $2 to $6 (tokens for 30 to 50 runs; function invocations are within the free tier or pennies)
- **Time:** about 5 hours
- **Done when:** a log of 20 runs, the number of steps and cost of each, and one run where the limit stopped the agent
- **Teardown:** delete the functions, roles, log groups and API endpoints

## L5.2: Run an MCP server in the cloud

- **Goal:** Write a small MCP server (two tools), run it in a container on a managed service, and call it from a client you wrote; secure it with authentication.
- **Services:** a container service (ECS Fargate at about $0.59 per day for 0.5 vCPU and 1 GB), a registry, a load balancer or function URL
- **Estimated cost:** $1 to $4 if deleted the same day (Fargate about $0.59 per day plus a load balancer about $0.73 per day)
- **Time:** about 4 hours
- **Done when:** a client that lists and calls both tools over the network, a failed call without credentials, and a note on what the server could do if its tool arguments were malicious
- **Teardown:** delete the service, the load balancer, the registry images and the logs
