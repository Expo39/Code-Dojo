# Workflows versus agents

*Reference explainer, checked against the official documentation in November 2026. Features and prices change quickly:
the tutor re-checks the live documentation before teaching from it.*

Anthropic's article "Building effective agents" (December 2024) sorts systems built on a language
model into two kinds:

- A **workflow** is a system in which your own code fixes the steps in advance. Example: call the
  model to summarise a support ticket, then call it again to draft a reply, then check the
  reply's length in code. The order never changes, whatever the ticket says.
- An **agent** is a system in which the model itself decides the steps as it goes: it chooses a
  tool (an action such as reading a file or running a search), looks at the result, and chooses
  the next one, with no fixed path.

Anthropic's advice is to use the simplest thing that works: often a single model call, or a
workflow. An agent is worth it only when the steps cannot be known in advance, for example fixing
a bug in a codebase you have never seen, because an agent costs more tokens, takes longer, and its
mistakes compound: an error in step 2 is carried into every later step. "Many tasks do not need an
agent" is the claim, not "agents are never needed".

Check: a nightly job turns yesterday's sales CSV file into a three-paragraph report, always in the
same format. Workflow or agent, and why?

## "Agentic workflow"

"Agentic workflow" is a loose industry term with no single official definition. It generally means
a process in which a language model does more than answer once: it takes several steps, uses tools,
and makes at least some of the decisions itself (what to do next, or whether its work is good
enough).

| Kind | Who decides the steps | Example |
| --- | --- | --- |
| Single call | nobody: one prompt, one answer | "Summarise this email" |
| Workflow (fixed chain) | your code, all of them | summarise, then draft a reply, then check its length in code |
| Agentic workflow | a mix: code sets the frame, the model decides some steps | draft a reply, have the model check it against the rules, loop until it passes or 3 tries are used |
| Agent | the model, all of them | "fix this bug": it chooses every action |

The term was popularised by Andrew Ng in 2024, with four patterns: **reflection** (the model checks
and improves its own output), **tool use** (it calls search, code execution or APIs), **planning**
(it breaks a task into steps itself) and **multi-agent** collaboration (several agents with roles).
Anything that uses one or more of these, beyond a single call, tends to be called agentic.

### The simplest way to tell them apart

One task, answering customer emails, done three ways:

1. **Workflow.** The program always runs the same steps: the model summarises the email, then
   writes a polite reply, then the program sends it. The model writes text but never chooses
   anything; every email goes through the same steps.
2. **Agentic workflow.** At some points the model decides what happens next: it reads the email and
   decides whether it is a refund request (then it looks up the order with a tool and replies), a
   complaint (then it hands it to a human) or a question (then it replies directly); then it checks
   its own reply and rewrites it if needed, at most 3 times. The code still sets the frame (the
   options, the tools, the limit of 3); inside that frame the model makes choices.
3. **Agent.** "Handle the inbox": the model decides everything, including which email to take
   first and what to look up.

The one question: does the model ever decide what happens next? Never: a workflow. Sometimes,
inside limits the code sets: an agentic workflow. Always: an agent. As a picture: a train (only
where the rails go), a bus on a fixed route whose driver may detour round a blocked road, a taxi
(wherever it judges best).

Check: where does an agentic workflow sit between a fixed workflow and an agent? Give one example.

## The five workflow patterns, with examples

Anthropic's "Building effective agents" names five common patterns. Each is an agentic workflow:
code (or a fixed procedure) sets the shape, and the model makes the decisions inside it.

| Pattern | The shape | General example |
| --- | --- | --- |
| **Prompt chaining** | step 1's output feeds step 2, and so on, with a check in code between steps (a **gate**) that stops the chain if a step failed | write a blog outline, check in code that it has every required section, then write the post from it |
| **Routing** | one model call classifies the input, then code sends it to the handler built for that class | support emails sorted into refund, bug report or question, each answered by its own prompt and tools; easy ones sent to a cheaper model |
| **Parallelisation** | independent pieces run at once, then the results are combined. Two kinds: **sectioning** (split one job into different parts) and **voting** (run the same job several times and compare) | sectioning: one call checks a pull request for security, another for style, another for tests; voting: three reviewers judge "is this code vulnerable?" and two out of three decides |
| **Orchestrator-workers** | a lead model decides what sub-tasks are needed (not known in advance), hands each to a worker, and combines the results | "add a field to the API": the lead finds the five files that need changes and gives each to a worker |
| **Evaluator-optimiser** | one call produces, another judges against criteria, and the loop repeats until it passes or a limit is reached | translate a text, have a second call score it against a glossary, retry up to 3 times |

The difference between orchestrator-workers and parallelisation: in parallelisation the pieces are
fixed in advance by the developer; in orchestrator-workers the model decides them for each task.

A sixth thing is not a pattern but a building block: the **augmented LLM**, a model with tools,
retrieval and memory. Every pattern above is made of these.
