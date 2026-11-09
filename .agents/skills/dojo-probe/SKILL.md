---
name: dojo-probe
description: Goal-first mini test that finds what a Code Dojo learner already knows and what they need for a goal, using the track's concept graph. Use when the learner says "probe me", "what do I need for X", "test what I know about X", "I want to start <track>", when a roadmap starts a new track, at the close of dojo-new-track, during placement (dojo-assess, before the practical check), or when the graph shows no evidence on concepts the next module depends on.
---

# Probe: what you want, what you hold, what is missing

A probe is measurement, not teaching: about 10 to 15 minutes in chat, no exercise files, no
timers on answers. It ends in a map of the learner's edges and a short path to their goal.
Everything waits for their "go" (`AGENTS.md`). Start the clock with `dojo.py start probe:<track>`.

## 1. Read the map first

Run `dojo.py graph` (every track together, including tracks the goal's concepts build on; it also
reads new log rows into the evidence). A goal in one track can rest on another's concepts
(robotics on C++ and Python): `graph path <goal>` lists those too, so probe them like any chain. Concepts that are
fluent, held or due are not probed again. Read `progress/BASELINE.md` and recent rows
of `progress/<track>/mistakes.md` and `progress/mistakes.md`: a known trap is the first place to look. With a prose record that has
not been read into the graph yet (`mistakes.md`, drill and mock reports, imported notes), propose
`graph set` lines from it as one list, with a `--ref` to the source, and write only the ones the
learner agrees with.

## 2. Make the goal concrete

Ask "What do you want to be able to do?" and keep asking, one question at a time, until the answer
names something observable ("solve two-pointer mediums in an interview", "read the team's
Django views"). Map it to goal concepts in the graph (a concept, a module, or an exercise) and say
it back in one line. If they do not know the subject well enough to say, the goal starts with an
overview of what the track covers: say so, and do not invent a goal for them.

## 3. Chains

Run `dojo.py graph path <goal>`. Group what is left into chains: prerequisites that build on each
other towards the goal (for two pointers: indexing → sorted order → Big-O). Show the learner the chain
names only, as a short outline, not the concepts.

## 4. Find each chain's edge

For each chain, look for the highest concept they hold and the lowest one they do not. Each
question is about one concept's `can` statement, always on a problem that is not an exercise
(hard rule 4), in one of three forms:

- **Predict**: 3 to 8 lines of code; "what does it print?" (two turns: the prediction first, the run
  or the reveal in the next message).
- **Choose**: 3 or 4 options of the same shape and length, with no reasoning in any of them;
  each wrong option is the answer one specific misconception gives.
- **Explain**: "in a few words, why ...?", graded against a short model answer.

Before asking, write the answer and its one-line reason in your draft of the report; grade against
that, not against how convincing their reasoning sounds. Every question asks for:

- **No confidence question.** Read it from the wording: a plain answer counts as sure (90), a
  hedged one as unsure (50). "I don't know" is always a fair answer: it is a gap, not a wrong
  answer, and it carries no confidence.
- **A few words of thinking**: what they noticed and what they were unsure of. Voice input is fine;
  read past transcription slips.

Choose the next question from the last one:

- Open near the top of the chain: start at the hardest concept the goal needs and let misses walk
  you down.
- Right and sure: jump well up. Right but unsure, or thin thinking: fragile; step up a little.
- Wrong: come down to find where it holds.
- Wrong and sure (80 or more): a misconception. Probe one or two neighbours to see how far it
  reaches before moving on; never correct it in the probe.
- A chain that never breaks: keep going up until it does, or until the goal is reached.
- Chains inform each other: never open a chain below what another has already shown.
- No filler: every question must move an edge. Do not re-ask what an answer already showed.

Reply neutrally during the probe (`AGENTS.md`, exercise loop step 2): say what was right, never
hint that something is off. The verdicts come at the end.

## 5. Record

- `dojo.py graph set <concept> <held|fragile|misconception|gap> --source probe --confidence N
  --note "<their words, short>"` for each concept the probe placed.
- `dojo.py mistake` for each misconception, with the correct form.
- `dojo.py done probe:<track>` (logged as study).
- The report, `progress/<track>/probes/<DD-MM-YYYY>_<goal>.md` (the goal in snake_case; a name
  already taken gets `_2`):
  1. **Goal**: in their words, and the goal concepts.
  2. **Chains**: per chain the floor (highest held), the ceiling (lowest missed), misconceptions,
     and where to build from.
  3. **Questions**: each with the concept, the form, the learner's answer in their words, the
     confidence, the verdict, and the model answer in words (never solution code).
  4. **Calibration**: how their confidence compared with their results (sure and right, sure and
     wrong, unsure and right).

## 6. From the map to a plan

Run `dojo.py graph path <goal>` again: that is the minimal path. Propose, as a short list:

- what to skip because it is held (`dojo.py mark <module> --box 3`, or `settings
  skip_modules+=<module>`; never skip a concept with a misconception);
- where to start, and which lessons come first (theory lessons for `theory` concepts, `teach me`
  for the rest, repairs for misconceptions first);
- the first exercises after that.

Agree it with the learner (`dojo-assess`, 3b); they have the last word. Log each change under
Plan changes in `PLAN.md`. Dates, mix or a new track go to `dojo-roadmap`.

## 7. Close

Four lines at their level: the goal, what they already hold (with evidence), the two or three
edges that matter most, and the first step. Then wait for their "go".
