# The context window, statelessness and chat history

*Reference explainer, checked against current provider documentation in November 2026. Model names, limits and prices change quickly: the tutor re-checks the live documentation before teaching from it.*

## Terms

- A **token** is the unit a model reads (about three quarters of an English word). Providers bill and
  limit in tokens, not words; each provider publishes a tokeniser or a token-counting call.
- The **context window** is the most tokens a model can take in and produce in one request: the
  instructions, the chat history, retrieved documents, the new question and the model's own answer, all
  together.

## When the input does not fit

Depending on the provider and the settings, an input that is too long is either rejected with an error or
silently cut, usually from the start, so the instructions can be the part that disappears. Local runtimes
often default to a small window and cut silently, so the symptom is a model that "forgets its rules".

## How to check that a prompt fits

1. Count instead of guessing, with the provider's token counter or the usage numbers in the response.
2. Size the worst case, not the average: the longest instructions, the most documents retrieved, the
   most history sent, the longest question and the longest answer. That total must fit with room to spare.
3. Log token counts in production and warn near the limit, because cutting can be silent.

## Fitting is not the same as being followed

Models follow rules less reliably as the prompt grows, and facts in the middle of a long prompt are used
less than those at the start or end: sometimes called **context rot**. It depends on how much text there
is, not on what fraction of the window is used, and small models feel it sooner. There is no magic
percentage such as "use half". Find the limit by measuring: run the evaluation set with the normal prompt
and a longer one, and compare the scores.

## The model is stateless

A model remembers nothing between requests. For each new message the program builds a prompt from scratch
and sends it; the model reads it, answers and forgets. A conversation feels continuous only because the
program chooses which earlier messages to send again.

## Deciding which history to send

Sending the whole history is simple but costs more with every turn and eventually does not fit. Options,
cheapest first: send the last N turns; summarise older turns into a short note; keep only the turns
relevant to the new question; store facts outside the chat (a database, a profile) and add only what the
question needs. Each choice trades cost against the risk of dropping something that mattered.

Check: a support chatbot works well for 5 messages and starts ignoring its own instructions by message
40. Name two likely causes and one measurement for each.
