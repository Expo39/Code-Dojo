"""Text adventure command router.

Level: easy
Target: 10

A text adventure reads one command per line. Write `route_command(command)` that
returns the game's reply, using a `match` statement:

- "go <direction>"  -> "You walk <direction>."
- "take <item>"     -> "You take the <item>."   (the item may be several words)
- "look"            -> "You look around."
- "quit"            -> "Goodbye."
- anything else     -> "I don't understand that."

    route_command("go north") -> "You walk north."

Trace by hand (work out the result yourself):

    [route_command(c) for c in ["look", "take rusty key", "go west", "quit"]] -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify route_command
"""


def route_command(command):
    raise NotImplementedError
