# Daily session

Pick the template that matches the time you have today (`python dojo.py today` names it).
The order matters more than the exact minutes: **retrieval first, new material while fresh,
performance practice, then logging**. Your own week (which day is for what, from your hours and
your track mix) is in `progress/docs/WEEK.md`; with several tracks, the "Learn and write" block
follows the mix that `today` shows.

Every session starts the same way: open the tutor in the repo (Claude Code, Codex or Gemini CLI). It runs the catch-up
automatically (what changed, what is due, the week balance). Say `start <exercise>` and
`done <exercise>` so the tracker can measure you.

## Full session (3 hours)

| Minutes | Block | What to do |
| --- | --- | --- |
| 0 to 10 | Warm-up | 3 cheat-sheet self-checks (`review the cheat sheet`), each with its setup stated, or one `predict drill` |
| 10 to 50 | Redo queue | Due items from blank files, in the order `today` lists them. Nothing due? Pull the oldest box-1 items |
| 50 to 110 | Learn and write | The next new module: `teach me <topic>` if it is new to you, then 2 or 3 new exercises |
| 110 to 120 | Break | Away from the screen |
| 120 to 150 | Read, debug or build | Alternate by day: a `bug drill` or `review drill` + one `m10` reading exercise, or 30 minutes on the current project |
| 150 to 170 | Perform | One unseen problem under interview conditions: a timer, out loud, no hints for the first 10 minutes (`interview problem`), or an `explain drill` |
| 170 to 180 | Log | Any mistakes, one cheat-sheet line per new concept, `end of day` to the tutor |

## Standard session (2 hours)

| Minutes | Block |
| --- | --- |
| 0 to 5 | Warm-up: 2 self-checks |
| 5 to 35 | Redo queue |
| 35 to 85 | Learn and write: one new concept and 2 exercises |
| 85 to 110 | Read/debug or project (alternate), or Perform on 2 days a week |
| 110 to 120 | Log |

## Short session (1 hour)

| Minutes | Block |
| --- | --- |
| 0 to 25 | Redo queue (the most overdue first) |
| 25 to 55 | One new exercise, or one talk-aloud timed problem |
| 55 to 60 | Log |

## Minimum day (30 minutes)

For bad days. It keeps the habit and the redo queue alive: 25 minutes of redo queue, 5 minutes
of logging. A minimum day counts; skipping does not.

## The weekly rhythm

| Day | Extra |
| --- | --- |
| One day mid-week | Replace the Perform block with an `explain drill` and a `review drill` on AI-written code |
| The last training day | **Mock interview** (45 to 60 minutes, `/dojo-mock`) replaces the Perform and Read blocks |
| End of the week | **Weekly review** (`/dojo-weekly`, 20 minutes): report, coach notes, next week's focus |
| Rest day | Rest. If the profile has a flexible rest day, training on it counts towards the week |

## Rules that make the time count

- Follow the checklists in `CHECKLISTS.md`: the exercise loop for every exercise, PRIMM for
  every new concept, the debugging loop for every bug. The tutor reminds you; the weekly report
  shows your process score.

- Type everything yourself. No AI completion in the editor while training (turn off Copilot
  and similar tools for this folder).
- Say the plan out loud before typing, even when alone. It is the interview habit, and it
  exposes gaps early. With voice dictation on (`/voice` in Claude Code), say it to the tutor instead of typing it.
- Predict before running a test. A wrong prediction is the most valuable minute of the day.
- When stuck past twice the target, ask for a hint. Struggling for an hour teaches less than a
  level-2 hint and a redo tomorrow.
- End every session with the log. The tracker only knows what you tell it.
