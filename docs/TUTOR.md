# Talking to the tutor

Run `claude` in the repo. The tutor coaches the method in `CHECKLISTS.md`: it asks you to
think out loud, asks for each step (understand, example, plan, predict, test, reflect), and
reminds you when you skip one. Tutor mode is on at the start of every session: the tutor explains,
asks questions, gives hints and reviews, but never writes your exercise or project code. Say
these in plain words; the tutor runs the tracker for you.

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
| `start <exercise>` | Timer starts; a fresh file appears in `workspace/<track>/` (a blank one for a redo) |
| `done <exercise>` | Tests run; time, hints and result are logged; the next redo is scheduled |
| `clarify <exercise>` | The interviewer's answers on edge cases, after you list your own |
| `pause` / `resume` | Stop the clock during a longer discussion (the tutor also does it for you) |
| `I'm stuck on ...` or paste an error | A hint at the lowest level that helps (the ladder in `METHOD.md`) |
| `done <LeetCode problem>` | Logged with your time and hints; it joins the redo queue too |
| `log mistake: ...` | Added to `progress/mistakes.md` |
| `end of day` / `how am I doing` | Today, the week, weak spots, and concrete advice for tomorrow |

## Learning

| Say | What happens |
| --- | --- |
| `teach me <topic>` | A PRIMM lesson: idea, predict a worked example, investigate, modify, then tiny typing tasks |
| `new exercise on <topic> [easy/medium]` | Fresh verified exercises in the right module |
| `more like <exercise>` | Same pattern, different story |
| `review my code` | Senior-engineer feedback on passing code, as questions and pointers |
| `review my project` | Design, tests and structure feedback on a project |
| `review the cheat sheet` | Self-check questions from `progress/cheatsheet.md`, oldest first |

## Reading, debugging, performing

| Say | What happens |
| --- | --- |
| `predict drill` | "What does this print?", three in a row |
| `trace drill` | Fill in a trace table of variables, iteration by iteration |
| `bug drill` | A new buggy function and a failing test in `workspace/drills/`; find it with the debugger |
| `review drill` | Code (often "written by an AI") with several problems: find them all |
| `explain drill` | Solve without code in five steps, scored |
| `explain drill: work` | Explain part of your current work project from memory; the tutor asks the hard follow-up questions (no work code is pasted) |
| `interview problem` | One unseen problem, timed, interviewer style |
| `mock interview` | A full 45 to 60 minute mock with scored feedback in `progress/mocks/` |

## Planning

| Say | What happens |
| --- | --- |
| `assess me` / `I already know ...` / `import my notes from <path>` | Placement: diagnostic, then `BASELINE.md`, `PLAN.md`, start module and redo queue updated |
| `weekly review` | Report, coach notes, next week's focus, plan updated |
| `am I on track for M1?` | Trend analysis and an honest re-estimate |
| `export` / `export to user@host:path` | Personal data zipped (and copied over SSH, or uploaded to Google Drive after `drive-setup`) |
| `TEACHER OFF` / `TEACHER ON` | Pause or resume tutor mode |

## Without the tutor

Everything works from the terminal too (`python dojo.py help`), and nothing is lost: the next
tutor session catches up with `sync`.

| Command | Purpose |
| --- | --- |
| `python dojo.py today` | Today's plan |
| `python dojo.py list [module]` | Exercises and their status |
| `python dojo.py start <ex>` / `test <ex>` / `done <ex> --hints N` | Do an exercise |
| `python dojo.py log study 45 <topic>` | Log time that is not an exercise (study, reading, drill, mock, project) |
| `python dojo.py week --write` / `stats` | Weekly report / modules, patterns and fluency gates |
| `python dojo.py export --to user@host:path` | Back up or move personal data |
| `python dojo.py drive-setup`, then `export` | Back up to Google Drive (see `SETUP.md`) |
