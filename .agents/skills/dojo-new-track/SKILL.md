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

1. **Scope.** The subject, who it is for (the roadmap's goal and bar, or "any learner"), the
   language or tool version that is current today (check the official site), and for a review,
   the existing `README.md`, `track.json` and module list.
2. **Search** (several searches in one turn, by keyword: "<topic> course syllabus", "<topic>
   free university course", "learn <topic> github"):
   - university courses: MIT OpenCourseWare, Stanford, Harvard (CS50), Helsinki MOOCs, Oxford,
     CMU, Berkeley and others;
   - the official documentation and tutorial; the language or tool's own learning material;
   - repositories on GitHub, GitLab and Codeberg (check stars, last commit, licence, archived);
   - free books and exercise platforms with feedback (for example Exercism).
3. **Judge every source; free is not the same as good.** For each: who made it (authority), how
   current it is (last update, the version it teaches), depth and correctness (spot-check the
   claims and run the code), exercise quality, licence, and fit with the dojo's method. Stars
   show popularity, not quality: a starred repo can be stale, shallow, unlicensed or wrong, and
   a small official one can be the best. **Niche topics need more care**: fewer good sources
   exist, so lean on official docs, standards, the maintainers' own tutorials and university
   courses, verify more, and say plainly when nothing good enough exists; then build from the
   official documentation.
4. **Synthesise, then improve.** Start from what the strongest sources agree on, then judge
   it: what do they all miss or teach badly (for example reading and debugging code someone
   else or an AI wrote, testing, current tools), what order would a learner really need, where
   is practice too thin? Fix those with your own reasoning, and say where you departed from the
   sources and why. One focus line per module; `Theory:` lines for background; projects from the best project ideas; current
   features of the current version, nothing deprecated. For a review: a list of proposed
   changes (add, move, update, remove), each with its reason and source, for approval before
   anything changes.
5. **Write**, in the format of `docs/TRACKS.md`:
   - `README.md`: a "Last reviewed: <date>, against <tool and version>" line at the top, phases,
     modules, milestones, Prerequisites, Theory, and a "Sources" table (what each source was used
     for, its licence). No time estimates.
   - `track.json` with `"reviewed": "<YYYY-MM-DD>"`.
   - Exercises are always original, written in the dojo format: never copy text, exercises or
     solutions, whatever the licence; structure, topic order and the *kind* of example may be
     borrowed, with the source credited.
6. **Build only what is needed now**: the first module (`dojo-new-exercise`), the rest as
   "planned". A review that adds lesson topics to a module that already has exercises also adds
   exercises for them, so no topic is taught without practice. **Be a good judge, and creative,
   before adding anything**, in this order: can an existing exercise take the new topic with a
   small change (type hints added to a function that already has an optional argument)? Can one
   new exercise train two or three topics together (a class with a class attribute that holds
   other objects)? Only then add an exercise, one per topic at most. Fold small topics into
   existing modules; remove or merge duplicates. More exercises are not a better course.
   Every addition, change and removal reaches learners as a question at their next session. Learners are told at their next
   session (new topics and exercises, also in modules they finished) and choose for each. Shared track files go in a pull request or commit; the learner's choices stay in
   `progress/`.
7. **Close**: the sources used and the ones rejected (one line why), the module list, and what
   was changed (or, for a review, what is proposed).
