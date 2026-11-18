# route_command: clarifications

Pattern: match-case

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- Upper and lower case do not matter ("GO East" works); the reply uses lower case ("You walk east.").
- Extra spaces before, after or between words are ignored.
- "go" takes exactly one word: "go" alone or "go north east" is not understood.
- "take" needs at least one word; several words are the item ("take rusty key" -> "You take the rusty key.").
- "look" and "quit" take no extra words: "look around" is not understood.
- Any direction word is accepted; there is no list of valid directions.
- Empty or unknown commands: "I don't understand that." (no exception).
