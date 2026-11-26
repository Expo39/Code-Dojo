"""A tool loop with a step limit.

Level: medium
Target: 30

An agent is a loop: the model sees the conversation and either calls a tool or gives its final
answer; the program runs the tool and shows the model the result. Write
`run_tool_loop(model, tools, question, max_steps)`:

- `model(messages)` returns a dict: `{"tool": name, "args": {...}}` to call a tool, or
  `{"final": text}` to finish. `messages` is a list of dicts, starting with
  `{"role": "user", "content": question}`.
- `tools` maps a name to a function; call it as `tools[name](**args)`.
- After each tool call, append `{"role": "tool", "name": name, "content": text}` to
  `messages` where `text` is `str(result)`. An unknown tool gives `error: unknown tool <name>`,
  and a tool that raises gives `error: <the exception's message>`; the loop goes on in both cases.
- The model may be called at most `max_steps` times. Return a dict: `answer` (the final text,
  or None), `steps` (how many times the model was called), `stopped` (`"final"` or
  `"step limit"`) and `messages` (the full list at the end).
- `max_steps` below 1: raise ValueError.

    replies = iter([{"tool": "add", "args": {"a": 2, "b": 3}}, {"final": "5"}])
    run_tool_loop(lambda m: next(replies), {"add": lambda a, b: a + b}, "2+3?", 5)
    -> answer "5", steps 2, stopped "final"

Trace by hand (the content of the last message, and the three values):

    replies = iter([{"tool": "div", "args": {"a": 1, "b": 0}}, {"tool": "div", "args": {"a": 4, "b": 2}},
                    {"final": "done"}])
    run_tool_loop(lambda m: next(replies), {"div": lambda a, b: a / b}, "go", 2) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify run_tool_loop
"""


def run_tool_loop(model, tools, question, max_steps):
    raise NotImplementedError
