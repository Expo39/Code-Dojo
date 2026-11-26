"""Check a model's tool call before running it.

Level: easy
Target: 15

A model chooses a tool's arguments, and it sometimes gets them wrong. Before running the tool,
check them and tell the model everything that is wrong at once, so its next try can fix it all.
Write `validate_tool_args(schema, args)`:

- `schema` maps an argument name to a dict with `type` (one of `"str"`, `"int"`, `"float"`,
  `"bool"`) and optionally `required` (True means it must be present; the default is False).
- `args` is the dict the model supplied.
- Return a list of error messages, in this order: first, for each schema name in schema order,
  a missing required argument or a wrong type; then each unknown argument in the order it
  appears in `args`. An empty list means the call is valid.
- Messages (exactly): `missing required argument 'x'`, `argument 'x' must be int, got str`
  (the schema type, then the real type name), `unknown argument 'x'`.
- A bool is not an int. An int is fine where a float is expected.

    schema = {"city": {"type": "str", "required": True}, "days": {"type": "int"}}
    validate_tool_args(schema, {"days": "3", "units": "c"})
    -> ["missing required argument 'city'", "argument 'days' must be int, got str", "unknown argument 'units'"]

Trace by hand (the exact list):

    validate_tool_args({"n": {"type": "float", "required": True}, "on": {"type": "bool"}},
                       {"on": 1, "n": True, "x": 0}) -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify validate_tool_args
"""


def validate_tool_args(schema, args):
    raise NotImplementedError
