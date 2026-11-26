# Try it: m05_tools_agents

Hands-on, 5 to 15 minutes each. Use any provider's free tier, a local model (for example Ollama) or a fake
model function, so nothing needs a GPU or a paid account unless a task says so. Done when the reading and recall
finish early; never instead of a discussion drill or an exercise. What you type goes in
`workspace/ai_engineering/m05_tools_agents/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Tool (function) calling** (`tool_calling`): Give a model one tool (a function returning the weather from a dict); handle its tool request in code; print the final answer.
- **The agent loop** (`agent_loop`): Extend that into a loop with three tools, a ten-step limit and a clear stop; log every step so you can read the whole run.
- **Designing tools for agents** (`tool_design`): Take a tool with five loosely typed arguments and redesign it with two typed arguments and error messages that tell the model how to fix its call.
- **The Model Context Protocol** (`mcp_protocol`): Run an existing MCP server (for example the filesystem one) from a client script or an MCP-capable app, list its tools and call one; note what you had to configure.
- **Multi-agent systems** (`multi_agent`): Split one research task into a planner and two workers (plain functions around a fake model); log the messages between them and count the calls.
- **Agentic RAG** (`agentic_rag`): Take your m04 pipeline and expose its search as a tool; let the model decide how many searches to run for three questions; compare cost and answers with the fixed pipeline.
- **Planning and reflection in agents** (`agent_planning`): Ask an agent to produce a plan before acting, then print plan against actions taken; note every step where it drifted from the plan.
