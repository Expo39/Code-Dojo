# run_tool_loop: clarifications

Pattern: bounded-loop

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- The model is called with the messages list as it stands; a call counts as a step whatever it returns.
- A final answer on the last allowed step is still a final answer.
- After `max_steps` calls without a final answer: answer None, stopped "step limit", and the messages so far (including the last tool result).
- A tool's result is turned into text with `str(...)`.
- A tool that raises any exception, or an unknown tool name, is reported to the model as a tool message beginning `error: `; the loop does not stop and the exception does not escape.
- `args` may be missing from a reply: treat it as no arguments.
- `max_steps` below 1 raises ValueError before the model is called.
