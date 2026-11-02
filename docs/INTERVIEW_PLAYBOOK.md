# Live-coding interview playbook

Interviews are unpredictable, so do not prepare for *questions*. Prepare a *process* that works
on any question, and practise it until it runs on its own under pressure. The weekly mock
(`/dojo-mock`) and the daily Perform block train exactly this.

## The process (every problem, every time)

| Step | Say and do | Why |
| --- | --- | --- |
| 1. Understand (2 to 4 min) | Restate the problem in your own words. Ask 2 or 3 questions: input size and types, empty input, duplicates, ties, invalid data, what to return when nothing matches | Most failed interviews solve the wrong problem. Questions also show seniority |
| 2. Example (2 min) | Work one small example by hand, out loud; add one edge case | It reveals the structure, and it is your test later |
| 3. Plan (3 to 5 min) | State the approach in two sentences and its complexity. Start with the simple correct version; mention the better one if you see it | The interviewer can steer you before you waste ten minutes |
| 4. Code (15 to 20 min) | Small steps, clear names, talk while typing ("now I collect the counts"). Parse first, then act | Silence is the enemy; clear names are free points |
| 5. Test (3 to 5 min) | Trace your example through the code line by line; then the edge case; fix calmly and say what was wrong | Finding your own bug is a strong signal, not a weak one |
| 6. Reflect (1 to 2 min) | Time and space complexity; what you would improve with more time | Shows you think beyond "it works" |

## Habits that fix the most common failures

- **Read structure from the data.** Never hard-code a value from the example (keys, lengths,
  names). Loop over what is actually there.
- **Parse, then act.** Pull every field of a record into variables first; decide only when the
  record is complete.
- **Collector, loop, return.** Make the result container before the loop, update it inside,
  return it after. Check the last line returns what was asked.
- **Run the example before saying done.** Out loud, line by line.
- **Stuck?** Say what you know, what you are unsure of, and the simplest thing you could do
  now. Then do it. A working brute force beats an unfinished clever solution.

## When you cannot write something

Say so calmly, then show you can still get to a correct result:

1. The concept and the approach in plain words.
2. A skeleton: the function, the loop, where the tricky part goes.
3. The precise thing you would look up ("the argument order of `str.split` with a limit").
4. How you would verify it: a test case, or running it on the example.
5. The trade-offs of the alternatives.

The `explain drill` scores you on these five steps.

## Questions they may ask about code you did not write

In the AI age this part matters more every year: *"What does this function do? What is wrong
with it? How would you test it?"* Train it with predict drills, review drills (often on
AI-written code with planted bugs) and the `m10_reading_code` exercises. Read top to bottom
first, name the inputs and outputs, trace one example, then look for edge cases.

## Confidence

Confidence in an interview comes from two things: having solved many similar problems
cleanly (the redo queue and `python dojo.py stats` show this, so look at them the day before),
and having been in the interview situation many times before (the weekly mocks). Neither
can be faked on the day, and both build steadily.

## Interview soon (the last 2 weeks before a real interview)

| When | Change |
| --- | --- |
| 14 to 4 days before | Stop new modules. Daily: 1 unseen easy-to-medium problem out loud with a timer, the redo queue, one `explain drill`. Mocks every other day. Read the company's stack and prepare 3 stories about your work (problem, what you did, result, what you learned) |
| 3 days before | Redo your 10 worst problems from blank files. Prepare questions for them |
| The day before | Light: two easy problems you know, review `progress/mistakes.md` and the cheat sheet. Sleep |
| The day | One easy warm-up problem 90 minutes before. Check the editor, camera and microphone. Then stop |
