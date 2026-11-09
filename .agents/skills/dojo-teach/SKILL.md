---
name: dojo-teach
description: Teach one concept to the Code Dojo learner using Predict-Run-Investigate-Modify-Make. Use when the learner says "teach me <topic>", "explain <concept>", or when a weak spot needs a lesson before more exercises.
---

# Teach a concept (PRIMM)

Wait for their "go" before running `primm` or teaching anything (`AGENTS.md`: everything waits for their go). Short lesson, then the learner types. Use an example from a DIFFERENT problem than any exercise. Follow the five PRIMM steps in order and never skip one. Every prediction (the example, a "what if", a modification, each Make task) is its own turn: ask for it, wait, and give the run command only in the next message; tell the learner which step they are on ("Step 2 of 5: Run") and what they need to show for it. Never explain before they have predicted.

0. **Where it sits**: find the concept in the track's concept graph and run `dojo.py graph path <concept>`. Every prerequisite still listed there comes first: a short repair if it is fragile or a misconception, its own lesson if it is a gap. Never re-teach what the graph shows as held or fluent; build on it. Show the learner the short path in one line ("you hold loops and dicts; today: counting, then grouping").
   **Lesson file**: the module is the concept's `module` (`tracks/<track>/<module>/primm/README.md` lists each module's lesson topics); the topic is the concept's `lesson`, so the finished lesson is read into the graph by itself. Run `dojo.py primm <module> <topic>`. It creates `workspace/<track>/<module>/primm/<topic>.<ext>` empty and starts a lesson timer; the learner types everything in it (the example, the modification and the Make tasks). Tell them the path. Never create ad-hoc scratch files elsewhere.
1. **The idea**, one reasoning step at a time: each step adds one fact to something the learner already holds (name it), small enough to land at once; a fact that cannot be derived from what they hold (a definition, a rule of the language) is stated plainly, without caveats, ideally as the answer to a question the example raises. After each step, one quick check question, and "what were you thinking while reading that?"; a wrong answer or a confused thought is repaired before the next step builds on it. In all, 3 to 5 plain sentences: what it is, when you reach for it, the one mistake people make with it. Check `progress/BASELINE.md` and the mistakes logs (`progress/<track>/mistakes.md`, `progress/mistakes.md`) for related past mistakes and address them. Start from the familiar: if `progress/<track>/revisits.md` lists an exercise this concept improves, name it as the bridge ("in X you built that with a loop; this is the short form"), without showing X's code. If the concept works differently in another language the learner uses, say so in one line.
2. **Predict**: show a short worked example (5 to 12 lines) and ask what it prints or returns, and how sure they are (0 to 100), before explaining. Wait for the answer. Right but unsure means fragile: one more small example before moving on. Wrong and sure (80 or more) is a misconception: log it (`dojo.py mistake`) and take it apart in step 3.
3. **Run and investigate**: let them run it in the module's lesson file (or the language's REPL, where it has one), then explain line by line where their prediction differed. Ask one "what if" question (change one input; what happens?).
4. **Modify**: ask them to change the example to do something slightly different. Review what they paste without rewriting it: point at lines, ask questions.
5. **Make**: 3 tiny typing tasks of increasing difficulty, one at a time ("write a function that ..."), checking each before the next.
6. **Lock it in**: name the dojo exercise(s) that use this concept next (`dojo.py list <module>`). Check `progress/<track>/revisits.md` for exercises the learner solved before knowing this concept; offer each as `<exercise>_revisited` (the same task, solved with the new concept), created with the `dojo-new-exercise` skill in this concept's module, and remove the line once it is solved. Then add one cheat-sheet bullet with a "Check:" question, and stop the timer: `dojo.py done lesson:<topic>` (logged as study; never estimate the minutes; the graph marks the concept held from it). If the Make tasks showed it is not held yet, record that instead: `dojo.py graph set <concept> fragile --source lesson --note "<what is still shaky>"`.
7. **Read next**: the official documentation section (for Python, the matching chapter of https://docs.python.org/3/tutorial/ or the library reference) and one follow-up question with a 2-line answer (a likely interview question when their mode involves interviews).

Pitch every step at the learner's level (`AGENTS.md`, Style): for a beginner, plain words, every term defined, smaller steps; for an advanced learner, fewer words and a harder Make task.

**Theory form** (a `Theory:` line from a module's `primm/README.md` or a track README, or the
learner asks for background such as Big-O, memory, a maths idea): the same steps, adapted, and
only as much theory as the next practical step needs (`docs/ROADMAP.md`, section 6). The idea
comes with a small table or picture in text; predictions may be answered on paper ("how many
steps for 1,000 items? for 1,000,000?"); Run is a short demo, a count or a measurement the
learner types; Modify and Make end in a few lines of code that use the idea. Name the lesson
after the theory concept's id in the graph (`theory_big_o`: `dojo.py primm <module> theory_big_o`),
so it is read into the graph by itself.

