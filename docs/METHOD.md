# Method: how the dojo teaches

The short version: **do, do not watch**. Every hour should end with code you wrote or code
you can explain line by line. The rules below come from learning research and from
experienced engineers' advice; sources are at the bottom.

## Twelve principles

1. **Retrieval beats re-reading.** Writing a solution from a blank file, days later, is what
   builds memory. Re-reading a solution feels productive and is not. That is why every exercise
   goes into a redo queue and comes back from a *blank* file.

2. **Spaced, not massed, and mixed.** Redos come back after 1, 3, 7, 14, 30 and 60 days
   (Leitner boxes). A clean solve moves an item up a box; a struggle sends it back to box 0. Aim
   for about half new material and half redos. The redo queue switches pattern and module from
   one redo to the next: recalling a method you used a minute ago trains nothing, while having to
   recognise which method a problem needs is the skill an interview tests. For the same reason a
   "more like X" exercise keeps the pattern and changes the story, and a drill pitched so that
   you get about 85% of its steps right teaches more than one you always or never get.

3. **Deliberate practice: just past your edge, with fast feedback.** Every exercise has tests,
   so feedback takes seconds. Targets are set so that you are slightly stretched. If something
   takes more than twice the target, stop, ask for a hint at the lowest level that helps, and
   schedule a redo.

4. **Predict before you run (PRIMM).** For each new concept: **P**redict what code does,
   **R**un it, **I**nvestigate (trace, debug, annotate), **M**odify it, then **M**ake your
   own. This builds the reading skill and the writing skill together, and it is how the tutor
   teaches a new topic.

5. **Worked examples first, then fade the help.** Novices learn faster from a clear worked
   example than from struggling blind. The tutor shows a concept on a *different* problem,
   then gives tiny typing steps, then a full exercise. Help fades as you improve: hints go
   from a question, to a concept, to a plan, to pseudocode, and only last to an explanation
   of a solution.

6. **Read as much as you write.** In the AI age you will read far more code than you type.
   Trace code by hand, predict its output, review code with planted bugs, and read real code
   (the standard library, small open-source projects). If you cannot explain a line, you do
   not understand the program.

7. **Build things (escape tutorial hell).** Exercises train moves; projects train the game.
   Every phase includes small projects with no step-by-step guide: you decide the structure,
   get stuck, and get unstuck. That is where confidence comes from.

8. **Train the performance, not just the knowledge.** Interviewing is a separate skill:
   solving while talking, under time pressure, with someone watching. If interviews are part of
   your goal, practise it from week 1 in small doses (talk-aloud timed problems, mocks as often
   as your mode says) so that the format is familiar long before it matters. As a hobby, skip it.

9. **Use AI as a tutor, never as a ghostwriter.** In Anthropic's 2026 randomised study,
   developers learning a new library with AI help scored 17 percentage points lower on
   understanding than those who coded unaided. Those who used AI to *ask conceptual questions
   and request explanations* kept their learning. So the tutor here explains, questions and
   reviews, and never writes your exercise code. The same rule works at a job where AI writes
   most of the code: read and explain every AI change *before* committing it, and ask the AI
   *why* when a line is unclear.

10. **Measure, and let the data steer.** Time against target, hints used, and clean solves are
    logged for every attempt. The weekly review reads the numbers, not feelings, and changes
    next week's plan. Confidence built on evidence survives a bad day; confidence built on
    hope does not.

11. **Start from what you hold, and build one step at a time.** Knowledge is a structure: a new
    idea that connects to nothing fades, one built on what you already hold stays. Each track has
    a concept graph (what each concept needs first), and a new goal starts with a short probe
    that finds where your understanding ends on each chain of concepts the goal depends on, so nothing you
    hold is taught again and nothing off the path is taught at all. Lessons then add one step at
    a time to something you already hold, with a check after each step, so a gap shows the
    moment it is stepped on, not three lessons later.

12. **Say when you are unsure.** Nobody asks for a number: a plain prediction or probe answer
    counts as sure, a hedged one ("I think", "maybe") as unsure. A wrong answer you were sure of is a misconception, the most useful thing a check can
    find, and it is repaired before anything builds on it; a right answer you were unsure of is
    fragile and gets one more check. Comparing how sure you sounded with your results
    (`stats`) trains you to know what you know, which is what an interviewer is probing too.

## Checklists

Every activity (an exercise, a new concept, a bug, unfamiliar code, a mock) follows a fixed
sequence of steps, in `CHECKLISTS.md`. The tutor coaches you through them and reminds you of
any skipped step; the tracker records skipped steps and the weekly report shows how often every
step was followed.

## The hint ladder

Ask for help at the lowest level that could unblock you. The tutor always says which level it
is giving, and the number of levels used is logged as "hints".

| Level | What you get |
| --- | --- |
| 1. Question | One question that points at the gap ("What should happen for an empty list?") |
| 2. Concept | The idea or tool, no code ("This is counting: a map from item to count", a dict in Python) |
| 3. Plan | The steps in plain English |
| 4. Pseudocode | The structure with blanks you fill in |
| 5. Walkthrough | The reference solution explained line by line; then you close it, write it from memory, and it goes to the redo queue for tomorrow |

## When you are stuck (on your own)

1. Reread the task and the test (1 minute).
2. Solve the example by hand; write the steps as comments; turn each comment into code (5 minutes).
3. Write the simplest version that works, even if ugly.
4. Runs but wrong? Set a breakpoint and compare every variable with what you expected (5 minutes).
5. Missing syntax? Look it up, close the page, type it from memory.
6. Ask the tutor for a hint. Do not stay stuck past twice the target time.

## Weekly balance

The shares hold for any number of hours and depend on the learner's mode (`ROADMAP.md`); the
daily templates in `DAILY_SESSION.md` follow this split.

| Strand | What it is | interview | hybrid | industry | hobby |
| --- | --- | --- | --- | --- | --- |
| Learn | new concepts with PRIMM, teach-me lessons, first attempts at new exercises | 20% | 25% | 25% | 30% |
| Write | the redo queue from blank files, plus new exercises | 25% | 25% | 20% | 20% |
| Read and debug | read drills, code reading, debug drills (often on AI-written code) | 20% | 20% | 20% | 15% |
| Build | the current project | 10% | 15% | 25% | 35% |
| Perform | a talk-aloud timed problem, mock interviews | 25% | 15% | 10% | 0% |

Mocks: weekly in `interview` mode, every two weeks in `hybrid`, monthly in `industry` once
applying is near, and only on request in `hobby`. Reading and debugging never drop below 15%:
with AI writing much of the code, it is the skill every mode needs.

## Sources

- Anthropic (2026), *How AI assistance impacts the formation of coding skills*:
  https://www.anthropic.com/research/AI-assistance-coding-skills
- Retrieval and spaced repetition applied to coding-interview practice (Red-Green-Code,
  LeetCode tips 9 and 10): https://www.redgreencode.com/leetcode-tip-9-spaced-repetition/ and
  https://www.redgreencode.com/leetcode-tip-10-planning-a-spaced-repetition-schedule/
- PRIMM (Sentance and Waite), Raspberry Pi Foundation summary:
  https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf
- Effective learning strategies and their limits for novices (Frontiers in Education, 2022):
  https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2022.996039/text
- Escaping tutorial hell by building projects (Real Python):
  https://realpython.com/how-to-get-out-of-tutorial-hell/
- Pattern-based interview preparation and mock interviews (NeetCode):
  https://neetcode.io/roadmap and https://blog.neetcode.io/p/prepare-coding-interviews
