---
name: dojo-new-track
description: Design a new Code Dojo track, or review an existing one, from the best free material on the web (university courses, official docs, well-regarded repos and books), judged critically and kept current. Use when the learner or a maintainer says "design a track for X", "build the X track", "review the X track", "is the X track up to date", when a roadmap reaches a placeholder track, or when doctor reports a track not reviewed for over a year.
---

# Design or review a track

The aim: the best possible course for learning the subject, not a match for the free ones.
Free courses, docs and repositories are inputs to judge, not a ceiling: use the strongest parts,
reject the weak ones, look beyond the sources named here, and use your own judgement (and the
dojo's method: practice, retrieval, reading code, projects) to fill their gaps and do better
than any one of them. Always in the dojo's own format, never a copy.

0. **Scope checklist** (`docs/CHECKLISTS.md`, section 8): before anything is searched or built,
   list what the track will cover and, separately, what it will not; the learner agrees or strikes
   each line. For an interview, the items come from its checklist (`dojo-interview-prep`). A new
   idea during the build is offered afterwards, never added.
   **Say what the subject means, and what it does not, in one or two lines, and get a yes before
   searching**: the same words name different subjects ("AI engineering" can mean building systems
   on top of models, or using AI tools to write code; "backend" can mean a language or a job). A
   track built on the wrong meaning wastes the whole build. Judge the meaning by who does the work
   (the job title, the product they ship), not by the tool they use.
1. **Scope.** Ask first: shared (`tracks/`, in git for everyone) or personal
   (`tracks_personal/`, gitignored, the learner's own: work material, a private course)? Its
   name must differ from every shared track's. A personal track is written in the same format
   and, when built for one learner, may target their goal directly; it never goes into git, and
   `export` backs it up. Then the subject, who it is for (the roadmap's goal and bar, or "any learner"), the
   language or tool version that is current today (check the official site), and for a review,
   the existing `README.md`, `track.json` and module list.
2. **Find, then read. A search result is a pointer, never evidence.**
   - **Find** (several searches in one turn, by keyword: "<topic> course syllabus", "<topic>
     free university course", "<topic> roadmap", "learn <topic> github"): university courses (MIT
     OpenCourseWare, Stanford, Harvard CS50, Helsinki MOOCs, Oxford, CMU, Berkeley and others); the
     official documentation and tutorial; the language or tool's own learning material; repositories
     on GitHub, GitLab and Codeberg; free books and exercise platforms with feedback (for example
     Exercism); community roadmaps and the table of contents of the standard book on the subject.
     Shortlist at least five sources of at least three kinds (a course, a book or roadmap, official
     documentation, a repository), and one that comes from the job itself (what practitioners are
     asked to do), not only from teachers.
   - **Read every shortlisted source for real.** Search snippets, summaries and your own memory
     of a course are not reading it. For each source:
     - open its actual syllabus, table of contents or lesson list **in full** (for a GitHub repository,
       `gh api repos/<owner>/<repo>/contents/<path> --jq .content | base64 -d` for its README, syllabus
       or table-of-contents file, and the folder listing of its lessons; for a web page, fetch it
       (WebFetch, or the `web-fetch` agent where you have no fetch tool of your own); for a book, its
       published table of contents or the author's repository);
     - open at least one real lesson, exercise and solution per source (not the title), and judge
       whether it teaches and tests or only shows;
     - verify the facts that matter with the tools, never from memory: stars, last push, licence,
       archived flag (`gh api repos/<owner>/<repo>`), the version the material teaches, the date of the
       last change;
     - say plainly what you could not read (paywalled, down, blocked) and treat that source as
       unread: it may shape a question to ask, never a module.
   - **Keep a reading log** while you work (in the scratchpad): per source, what you opened, what you
     read in full and what only in part. The final report in step 7 lists it. If the log does not
     show that a source was opened, the report cannot say what it teaches.
3. **Judge every source; free is not the same as good.** For each: who made it (authority), how
   current it is (last update, the version it teaches), depth and correctness (spot-check the
   claims and run the code), exercise quality, licence, and fit with the dojo's method. Stars
   show popularity, not quality: a starred repo can be stale, shallow, unlicensed or wrong, and
   a small official one can be the best. **Niche topics need more care**: fewer good sources
   exist, so lean on official docs, standards, the maintainers' own tutorials and university
   courses, verify more, and say plainly when nothing good enough exists; then build from the
   official documentation.
4. **Synthesise from a coverage matrix, then improve.** Build a table from what you read: one row
   per topic, one column per source, marking where each source teaches it and how deeply. A topic
   that two or more independent sources teach is part of the subject unless you can say why not;
   a topic only one teaches needs a reason to be in. Check the matrix against the meaning agreed in
   step 0, and cut or flag anything that belongs to another subject. **Show the learner the module
   list and the matrix's gaps and get a yes before writing content.** Then judge it against the dojo's own method (`docs/METHOD.md`: retrieval, spaced redos, practice before explanation, reading and debugging, projects), because the best course for any subject is not the best-looking syllabus but the one that makes the learner able to do the work:
   what do they all miss or teach badly (reading and debugging code someone else or an AI wrote,
   testing, current tools), what order does a learner really need, where is practice too thin?
   Fix that with your own reasoning and say where and why you departed from the sources. One
   focus line per module, `Theory:` lines for background, projects from the best ideas, current
   features only. A review ends in a list of proposed changes (add, move, update, remove), each
   with its reason and source, approved before anything changes.
5. **Write**, in the format of `docs/TRACKS.md`:
   - `README.md`: "Last reviewed: <date>, against <tool and version>" at the top; phases, modules,
     milestones, Prerequisites, Theory, and a "Sources" table (what each was used for, why it is
     trusted). No time estimates.
   - `track.json` with `"reviewed": "<DD/MM/YYYY>"` and `"builds_on"`: the tracks it is built on
     (a library or framework track names its language, e.g. `["python"]` for pandas; ROS names
     `["cpp", "python"]`). A library is its own track beside its language, never a folder inside it.
   - `graph.json`, the concept graph (`docs/TRACKS.md`, "Concept graph"): every concept the
     modules teach, what each needs first (`requires`), an observable `can` statement, its
     `lesson` (a topic of the module's `primm/README.md`; `kind: theory` for `Theory:` lines) and
     its exercises; planned modules' concepts marked `"planned": true`. **Coverage check before
     closing**: every topic that two or more sources teach is a concept in the graph, or is listed
     in the README as left out, with the reason. A concept that holds in any
     language and already exists in another track's graph (Big-O, recursion, two pointers, BFS)
     reuses that `id`, `name` and `can` with `"shared": true`, so what the learner knows from the
     other track counts here too; language rules are never shared. A concept that builds on
     another track's (robotics on C++ pointers, a web framework on Python classes) names it in
     `requires` as `<track>:<id>`, so the combined graph shows how the tracks connect. `dojo.py graph check
     <track>` must report no errors. A review updates it with the modules.
   - Exercises are original, in the dojo format: never copy text, exercises or solutions,
     whatever the licence; structure, topic order and the *kind* of example may be borrowed,
     credited.
6. **Exercises: judge before adding, and add little.** No topic without practice, but in this
   order: can an existing exercise take the topic with a small change (type hints on a function
   that already has an optional argument)? Can one exercise train two or three topics (a class
   with a class attribute that holds other objects)? Only then a new exercise, at most one per
   topic; merge or remove duplicates. More exercises are not a better course. A new track gets
   its first module only (`dojo-new-exercise`), the rest "planned". Every exercise is listed under
   the concept it trains in `graph.json`. Shared exercises are not
   acknowledged for any learner: each is asked at their next session if the module is one they
   have started, and meets it on arrival otherwise.
7. **Close**: the reading log (each source, what was read in full and what only in part, what could
   not be read), the sources used and the ones rejected (one line why), the coverage matrix's result
   (topics in two or more sources and where each went), the module list, and what was changed (or,
   for a review, what is proposed). For a learner about to start the track,
   offer the probe (`dojo-probe`): their goal in it, and what they already hold, before the first
   module.
