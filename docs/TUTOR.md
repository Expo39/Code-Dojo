# Talking to the tutor

Run `claude` in the repo (or `codex`, or `gemini`: the same rules, see `SETUP.md`). The tutor coaches the method in `CHECKLISTS.md`: it asks you to
think out loud, asks for each step (understand, example, plan, predict, test, reflect), and
reminds you when you skip one. Tutor mode is on at the start of every session: the tutor explains,
asks questions, gives hints and reviews, but never writes your exercise or project code. Say
these in plain words; the tutor runs the tracker for you, except the tests, which you run and
read yourself (it gives you the command). Nothing starts until you say **go**: the tutor names
the next block or exercise (a warm-up check, a redo, a drill, a lesson, a mock, an interview
problem) and waits; no file, problem or timer appears before your go. If the tutor misunderstands
you and it costs you time, it says so and gives the minutes back (`done --credit M`), so your solve
time stays fair.

## Talk, do not type

Turn on voice dictation once with `/voice`, then hold the spacebar while you speak. Use it for
everything you would say out loud in an interview: the restatement, your hand trace, the plan,
your prediction, the reflection, and your answers in drills and mocks. Speaking is faster than
typing, and it trains the habit of thinking out loud. Code is still typed by you, in the editor:
dictated code does not count as typing it yourself.

## Every day

| Say | What happens |
| --- | --- |
| (your first message) | Catch-up: work done without the tutor gets logged, then today's plan |
| `start <exercise>` | Timer starts; a fresh file appears in `workspace/<track>/<module>/` (a blank one for a redo; the old one goes to that module's `.history/`) |
| `done <exercise>` | Tests run; time, hints and result are logged; the next redo is scheduled |
| (your prediction) | Say how sure you are too (0 to 100; "I don't know" is fine). The tutor gives you the command, `! python dojo.py test <exercise>`; you run it and read the output yourself. On a failure you read the last line of the error out loud before the tutor points at anything |
| `clarify <exercise>` | The interviewer's answers on edge cases, after you list your own |
| `pause` / `resume` | Stop the clock during a longer discussion (the tutor also does it for you) |
| `break` / `I'm away` / work on the dojo itself | The session clock pauses (only training counts) and resumes when you are back |
| `I'm stuck on ...` or paste an error | A hint at the lowest level that helps (the ladder in `METHOD.md`) |
| `done <LeetCode problem>` | Logged with your time and hints; it joins the redo queue too |
| `log mistake: ...` | Added to the track's `progress/<track>/mistakes.md`, or to `progress/mistakes.md` when it holds in any language |
| `end of day` / `how am I doing` | Today, the week, weak spots, and concrete advice for tomorrow; at the end of the day the session clock stops and the training outside exercise timers is logged as study |

## Learning

| Say | What happens |
| --- | --- |
| `probe me` / `what do I need for <X>?` | A 10 to 15 minute mini test in the chat: what you want to be able to do, then a few questions (predict, choose, explain in a few words, each with how sure you are) that find where your understanding ends; then the shortest path to your goal, agreed with you. A report goes in `progress/<track>/probes/` |
| `what can I do next` / `show my graph` / `how do I get to <X>?` | The concept graph: what you can start now, your state on every concept (`python dojo.py graph --html` for a page you can click through), or the fewest concepts still to learn for a goal |
| `teach me <topic>` | A PRIMM lesson that starts from what you already hold: idea (one step at a time, with a quick check after each), predict a worked example, investigate, modify, then tiny typing tasks, typed in `workspace/<track>/<module>/primm/<topic>.<ext>`; the lesson is timed and counts as study time |
| `new exercise on <topic> [easy/medium]` | Fresh verified exercises in the right module |
| `design a track for <subject>` / `review the <X> track` | The tutor researches the best free courses, docs and repositories, keeps only what is good and current, and builds (or proposes changes to) the track, citing its sources |
| `more like <exercise>` | Same pattern, different story |
| `review my code` | Senior-engineer feedback on passing code, as questions and pointers |
| `review my project` | Design, tests and structure feedback on a project |
| `review the cheat sheet` | Self-check questions from your cheat sheets (`progress/<track>/cheatsheet.md` and `progress/cheatsheet.md`), oldest first |

## Reading, debugging, performing

| Say | What happens |
| --- | --- |
| `predict drill` | "What does this print?", and how sure you are, three in a row |
| `discriminate drill` | Two or three problems that look alike but need different patterns: name each pattern and the detail that decides it |
| `practise <concept>` | A mixed set of drills on concepts from the graph: recall first, then telling it apart from a look-alike, then using it with others |
| `trace drill` | Fill in a trace table of variables, iteration by iteration |
| `debug this` / a breakpoint | In the editor, "Debug: this file" (Zed F4, VS Code Run and Debug) works on any exercise, drill, mock or lesson; without an editor, `breakpoint()` and `python dojo.py debug <file>` in your own terminal (`SETUP.md`) |
| `bug drill` | A new buggy function and a failing test in `workspace/<track>/drills/bug/`, named after the function; find it with the debugger |
| `review drill` | Code (often "written by an AI") in `workspace/<track>/drills/review/` with several problems: list them all, then compare your list with the real issues in the report (no fixing: that is what bug drills train) |
| (after any drill) | A report in `progress/<track>/drills/`: your answer in your words, the real issues, and what you found, found after a prompt, missed or flagged wrongly |
| `explain drill` | Solve without code in five steps, scored |
| `explain drill: work` | Explain part of your current work project from memory; the tutor asks the hard follow-up questions (no work code is pasted) |
| `interview problem` | One unseen problem, timed, interviewer style |
| `mock interview` | A full 45 to 60 minute mock with scored feedback in `progress/<track>/mocks/` (scheduled by your mode, or any time you ask). As on an interview platform you get a starter file (problem, examples, signature) and its sample tests in `workspace/<track>/mocks/<type>/` (pattern, practical, bug or explain), named after the problem and the date; the interviewer keeps hidden cases for the end |

## Planning

| Say | What happens |
| --- | --- |
| `set me up` (first time) | The tutor asks your mode, target level, time and track in the chat, runs `python dojo.py setup` for you, then goes on to placement |
| `show my modules` | Your modules (assigned, left out, planned) with your progress; say which to leave out or add, and the tutor talks it through with you: your reason, its view, then you decide together |
| `show my settings` / `change <setting> to <value>` | Every setting at a glance (`python dojo.py settings`), or any one changed: minutes per day, mode, target level, tracks, dates, skipped modules |
| `assess me` / `I already know ...` / `import my notes from <path>` | Placement: a probe and a short practical check, then `BASELINE.md`, `PLAN.md`, start module and redo queue updated |
| `plan my learning` / `I want to learn <X>` / `when should I start <X>?` / `replan` | Roadmap: the tutor asks what is missing about your goals, recommends the order and mix of tracks with reasons and the cost, and records your choice (`docs/ROADMAP.md`) |
| `change my mode to <hobby/industry/...>` / `I want to be a <junior/mid/...> developer` | Mode or target level updated; the weekly balance, mocks and bars follow (`docs/ROADMAP.md`) |
| `I have an interview on <date>` / `focus on <X>` | The priority changes: that track takes most of the time, the others keep only their redos |
| `weekly review` | Report, coach notes, next week's focus, plan updated, and settings changes suggested from your log for you to accept or decline, one yes-or-no question each |
| `am I on track?` | Trend analysis against your own bar and milestones, and an honest re-estimate |
| `update` | The incoming shared changes are shown (and which files run code); after your yes they are pulled in; new or changed exercises in your tracks are listed, and for each group you say: learn it, already know it, or not for me |
| `export` / `export to user@host:path` | Personal data in one zip, with a view of each concept graph inside it, (and copied over SSH, or uploaded to Google Drive after `drive-setup`) |
| `TEACHER OFF` / `TEACHER ON` | Pause or resume tutor mode |

## Without the tutor

Everything works from the terminal too (`python dojo.py help`), and nothing is lost: the next
tutor session catches up with `sync`.

| Command | Purpose |
| --- | --- |
| `python dojo.py setup` | First time: installs, asks your settings, checks, says what comes next |
| `python dojo.py settings [key=value ...]` | Show or change any setting; `--review` suggests changes from your log |
| `python dojo.py today` | Today's plan |
| `python dojo.py modules` | Your modules: assigned, excluded, before your start, planned |
| `python dojo.py update` / `changes` | Pull shared updates / see new, changed or removed exercises since you were last asked |
| `python dojo.py list [module]` | Exercises and their status |
| `python dojo.py start <ex>` / `test <ex>` / `done <ex> --hints N` | Do an exercise |
| `python dojo.py log study 45 <topic>` | Log time that is not an exercise (study, reading, drill, mock, project) |
| `python dojo.py week --write` / `stats` | Weekly report / modules, patterns, confidence against results and fluency gates |
| `python dojo.py graph [--html]` / `graph next` / `graph path <X>` | Your state on every concept / what you can do now / the shortest path to X |
| `python dojo.py export --to user@host:path` | Back up or move personal data |
| `python dojo.py drive-setup`, then `export` | Back up to Google Drive (see `SETUP.md`) |
