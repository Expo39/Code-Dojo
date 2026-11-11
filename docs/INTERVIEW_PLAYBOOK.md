# Live-coding interview playbook

For learners whose goal includes interviews (mode `interview` or `hybrid`, or an interview that
comes up). Interviews are unpredictable, so do not prepare for *questions*. Prepare a *process*
that works on any question, and practise it until it runs on its own under pressure. Mocks
(`/dojo-mock`) and the Perform block train exactly this. When a real interview comes, tell the
tutor the company and what it is known to test: the bar is set from that standard
(`ROADMAP.md`), and your prep goes in `progress/docs/INTERVIEW_PREP.md`.

## The process (every problem, every time)

| Step | Say and do | Why |
| --- | --- | --- |
| 1. Understand (2 to 4 min) | Restate the problem in your own words. Ask 2 or 3 questions: input size and types, empty input, duplicates, ties, invalid data, what to return when nothing matches | Most failed interviews solve the wrong problem. Questions also show seniority |
| 2. Example (2 min) | Work one small example by hand, out loud; add one edge case | It reveals the structure, and it is your test later |
| 3. Plan (3 to 5 min) | State the approach in two sentences and its complexity. Start with the simple correct version; mention the better one if you see it | The interviewer can steer you before you waste ten minutes |
| 4. Code (15 to 20 min) | Small steps, clear names, talk while typing ("now I collect the counts"). Parse first, then act | Silence is the enemy; clear names are free points |
| 5. Test (3 to 5 min) | Trace your example through the code line by line; then the edge case; fix calmly and say what was wrong | Finding your own bug is a strong signal, not a weak one |
| 6. Reflect (1 to 2 min) | Time and space complexity; what you would improve with more time | Shows you think beyond "it works" |

## When you are stuck

Say what you know, what you are unsure of, and the simplest thing you could do now. Then do it.
A working brute force beats an unfinished clever solution. The habits that fix *your* most
common failures come from your own mistakes and mocks; they are in `progress/docs/PITFALLS.md`
and, when an interview is a goal, `progress/docs/INTERVIEW_PREP.md`.

## When you cannot write something

Say so calmly, then show you can still get to a correct result:

1. The concept and the approach in plain words.
2. A skeleton: the function, the loop, where the tricky part goes.
3. The precise thing you would look up ("the argument order of `str.split` with a limit").
4. How you would verify it: a test case, or running it on the example.
5. The trade-offs of the alternatives.

Use it inside a problem, for the part you are stuck on, and keep it to a minute or two;
then write what you can. It is a move in `interview problem` and mocks, not an exercise of its own.

## Questions they may ask about code you did not write

In the AI age this part matters more every year: *"What does this function do? What is wrong
with it? How would you test it?"* Train it with read drills, debug drills (often on
AI-written code with planted bugs) and the `m10_reading_code` exercises. Read top to bottom
first, name the inputs and outputs, trace one example, then look for edge cases.

## Your current project

Almost every interview asks you to walk through your current work. Be able to draw its
architecture on paper and explain its trickiest part, and the reasons behind it, without
notes. If AI wrote much of it, this needs deliberate effort: the `work drill` trains it.

## Confidence

Confidence in an interview comes from two things: having solved many similar problems
cleanly (the redo queue and `python dojo.py stats` show this, so look at them the day before),
and having been in the interview situation many times before (the mocks). Neither
can be faked on the day, and both build steadily.

## Interview soon (the last 2 weeks before a real interview)

| When | Change |
| --- | --- |
| 14 to 4 days before | Stop new modules. Daily: 1 unseen easy-to-medium problem out loud with a timer, the redo queue. Mocks every other day. Read the company's stack and prepare 3 stories about your work (problem, what you did, result, what you learned) in `progress/docs/INTERVIEW_PREP.md` |
| 3 days before | Redo your 10 worst problems from blank files. Prepare questions for them |
| The day before | Light: two easy problems you know, review your mistakes logs and cheat sheets (`progress/` and `progress/<track>/`). Sleep |
| The day | One easy warm-up problem 90 minutes before. Check the editor, camera and microphone. Then stop |
