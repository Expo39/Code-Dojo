# Checklists

Every activity in the dojo follows a fixed sequence of steps. The steps are the method: they
are what makes practice turn into skill, and they are exactly what interviewers watch for.
The tutor coaches you through them, asks you to think out loud, and reminds you when a step is
skipped. The tracker records skipped steps (`done --skipped plan,predict`), and the weekly
report shows how often you followed every step, next to your speed.

Rule for all of them: **say what you are thinking, out loud, all the time.** Silent work cannot
be coached, and silent candidates cannot be assessed.

## 1. Exercise loop (every exercise, every problem)

The same six steps as the interview process (`INTERVIEW_PLAYBOOK.md`), with "predict" added
because it is the step that trains reading.

| # | Step | You show | Done when |
| --- | --- | --- | --- |
| 1 | **Understand** | The task in your own words, naming the exact condition (`> 0` or `>= threshold`?) and what is returned (a value, an index, a list); 1 to 3 questions about input, empty cases, duplicates, invalid data. The task text deliberately leaves edge cases out: ask the tutor, or list yours and then compare with `python dojo.py clarify <exercise>` | You could explain the task to someone who has not read it |
| 2 | **Example** | The task's `Trace by hand:` input (printed without its output) worked through your plan, plus one edge case of your own; for an outside problem, a small input you make up. Write it down (comments in the file or paper) when indexes are involved: written slices are easier to get right than spoken ones | You know the expected output of both |
| 3 | **Plan** | The approach in 1 or 2 sentences and its rough complexity, before typing | The plan is specific enough that someone else could code it |
| 4 | **Predict** | Before each test run: "it will pass" or "test X will fail because ...". Only then does the tutor give the test command, and you run it yourself. On a failure, read the error and try your own fix first; ask the tutor when stuck | You said it out loud before pressing Enter |
| 5 | **Test** | Your example traced through your code line by line, then the edge case | Both give the expected output, by trace and by the tests |
| 6 | **Reflect** | Time and space complexity; the input that would break it; one improvement | You could defend the solution to an interviewer |

Code (between steps 3 and 4) happens in small pieces, narrated: "now I collect the counts".

Typing your thinking to the tutor is slower than saying it: keep answers short (a few words,
bullets). For a longer discussion that is not solving, the tutor pauses the clock
(`python dojo.py pause`, then `resume`), so the time against target stays fair. Mocks are never
paused: there, the clock is part of the test.

## 2. New concept: PRIMM

Used by `teach me <topic>` and by the `r` (read and predict) exercises.

| Step | You do | Why |
| --- | --- | --- |
| **Predict** | Read a short example and say what it will do, before running it. Commit to an answer | A committed guess makes the surprise stick |
| **Run** | Run it and compare with your prediction | Feedback in seconds |
| **Investigate** | Explain why it behaves that way; answer "what if" questions; trace it | Turns "I saw it" into "I understand it" |
| **Modify** | Change the working example to do something slightly different | Practise in a safe space before a blank page |
| **Make** | Write something new with the concept, from a blank file | The real test: can you produce it? |

Never skip **Predict**: running code you have not predicted teaches almost nothing.

## 3. Debugging loop (every bug, every failing test)

| # | Step | You show |
| --- | --- | --- |
| 1 | **Read** | The last line of the traceback, out loud: the error type and message. Then the frame in *your* file |
| 2 | **Reproduce** | The smallest input that shows the bug |
| 3 | **Hypothesise** | "I think X is wrong because Y", before changing anything |
| 4 | **Confirm** | A breakpoint or `print` that proves or disproves the hypothesis |
| 5 | **Fix** | The smallest change; then rerun the tests |
| 6 | **Name** | The bug class (off-by-one, mutable default, early return, ...) and how to avoid it next time |

Changing code before step 3 is guessing, not debugging.

## 4. Reading unfamiliar code

| # | Step |
| --- | --- |
| 1 | What goes in and what comes out (the signature, the return statements) |
| 2 | The main loop or flow, in one sentence |
| 3 | One small input traced by hand |
| 4 | Edge cases: empty, one item, duplicates, invalid values |
| 5 | What you would ask the author, or what you would change |

## 5. Mock interview

The exercise loop under interview conditions, plus: greet, ask questions at the end, and stay
calm when stuck (say what you know, what you are unsure of, the simplest next step). Scored by
`dojo-mock` on understanding, approach, code, testing and communication.

## 6. End of every session

| # | Step |
| --- | --- |
| 1 | Every attempt logged with hints and skipped steps |
| 2 | Mistakes logged in words ("what went wrong" and "correct form") |
| 3 | One cheat-sheet line per new concept, with a self-check question |
| 4 | Say tomorrow's first task |

## 7. All the good practices, and what the tutor does if one is skipped

The checklists above are the step-by-step part. These are every other practice the dojo is
built on (`METHOD.md`, `DAILY_SESSION.md`, `INTERVIEW_PLAYBOOK.md`). The tutor watches for all
of them and gives a one-line reminder when one slips; the tracker nudges where it can detect it.

| Practice | When | If skipped, the tutor / tracker |
| --- | --- | --- |
| **Think out loud** | Always | Asks "Talk me through your thinking" before reacting to code or answers |
| **Redo queue before new material** | Every session | `start` warns if redos are due and you open a new exercise; the tutor suggests the queue first |
| **Blank file for redos** | Every redo | `start` gives a fresh file; the tutor reminds you not to open `.history/` or old notes |
| **Main method first, follow-up as a bonus** | Redos with an entry in `progress/approaches.md` | Main method from the blank file first; only after it passes with time left, the tutor invites the follow-up method and says which trade-off it wins |
| **Type it yourself, no AI completion** | All exercises and projects | Reminds you; `.vscode/settings.json` and `.zed/settings.json` turn inline suggestions off, and `.claude/settings.json` turns off Claude Code's suggested replies in the prompt |
| **Exercise loop** (understand, example, plan, predict, test, reflect) | Every exercise and outside problem | Asks for the missing step; logs it with `--skipped` |
| **PRIMM** for new concepts | Every new topic | `teach me` always runs the five steps in order; never explains before you predict |
| **Run the tests and read the errors yourself** | Every test run | Gives you the `dojo.py test` command instead of running it; asks you to read the last line of the error before pointing at anything |
| **Debugging loop** (read, reproduce, hypothesise, confirm, fix, name) | Every bug and failing test | Stops a code change made before a hypothesis: "What is your hypothesis?" |
| **Read structure from the data; parse, then act; collector, loop, return** | Every solution | Points at the line with a question when a value is hard-coded or a return is missing |
| **Hint at twice the target, not later** | When stuck | `done` flags attempts over twice the target with no hint; the tutor offers hint 1 at 2x |
| **Hints from the lowest level** | When stuck | Always starts at level 1 and says the level |
| **Log every attempt, mistake and new concept** | End of each task | Runs `done`, `mistake` and adds the cheat-sheet line; asks "Any mistakes on the way?" |
| **Balance the strands** (learn, write, read and debug, build, perform) | Every week | The weekly review checks the split and moves the next week's blocks |
| **Perform regularly** (timed problem, weekly mock) | Most days; weekly | `dojo-session` reminds on mock day; the weekly review notes a missed mock |
| **Projects: smallest working version first, commit each step, tests from P2** | Projects | `review my project` checks commits, structure and tests |
| **AI as tutor, never ghostwriter** | Always, also at work | Never writes your code; at work: explain each AI diff before committing, debug first (`WORK_HABITS.md` if present) |
| **Sustainable pace** (minimum day instead of skipping, rest day, sleep) | Every week | `today` caps catch-up at an hour a day; the weekly review adjusts the plan instead of piling up debt |
