# How a model produces an answer

*Reference explainer, checked against current provider documentation in November 2026. Model names, limits and prices change quickly: the tutor re-checks the live documentation before teaching from it.*

## Next-token prediction

A language model does one thing: given all the text so far, it predicts the next **token**. A token
is the unit a model reads, roughly three quarters of an English word; code, numbers and rare words
split into more pieces. At each step the model gives every possible next token a probability (after
"The cat sat on the": "mat" 40%, "floor" 20%, "sofa" 10% ...), one token is picked, it is added to the
text, and the model predicts again. There is no separate step where "the answer" is chosen: the answer
is the continuation of the text.

This is why a prompt can end on an unfinished line to force a short answer. A classification prompt
that ends with `Ticket: "my card was charged twice"` and `Category:`, after several examples where
`Category:` was followed by one word, makes a category word by far the most likely continuation.

## Sampling parameters

- **Temperature** controls how random the pick is. At 0 the most likely token is always taken, so the
  same prompt gives (nearly) the same answer, which suits extraction, classification and code. Higher
  values sometimes pick less likely tokens, which suits brainstorming and creative writing.
- **Top-p** (nucleus sampling) limits the pick to the smallest set of tokens whose probabilities add up
  to p, so very unlikely tokens are never chosen. Providers usually advise changing temperature or
  top-p, not both.
- **Max tokens** caps the length of the answer; hitting it cuts the answer off mid-sentence.
- A fixed **seed**, where the provider supports one, makes runs more repeatable, but "temperature 0"
  does not guarantee byte-identical answers across runs, hardware or model versions.

## Few-shot prompting

Putting a few solved examples (an input and its right output) in the prompt is **few-shot
prompting**. It shows the exact format and the borders between close categories, and it helps small
models most.

## Keep test questions out of the prompt

An **evaluation set** is a list of test inputs with known right answers, used to measure how often the
system is right. If a test input also appears as a worked example in the prompt, the model copies the
answer and the score is **inflated**: it no longer measures behaviour on new inputs. Write prompt
examples separately from evaluation cases.

## Descriptions decide the choice

When a model picks a tool, a route or a category, it decides from the descriptions it can see, and only
from those. A good description says what the thing is for, when to use it, and, if a close neighbour
exists, what it is not for. A vague description invites the wrong choice, even from a strong model.

## Never trust the output as it is

A prompt only makes the right answer likely. The program around the model checks the reply in code: it
caps the length, validates the shape, searches for an allowed value, falls back to a safe default, and
validates anything that will be executed or stored.

Check: a classifier prompt gives 20 examples and you score it on 100 labelled inputs, 15 of which are
the same as the examples. Why is the score unreliable, and how do you fix the measurement?
