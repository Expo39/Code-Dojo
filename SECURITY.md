# Security

Please do not open a public issue for a security problem. Report it privately instead:
**Security → Report a vulnerability** on this repository's GitHub page. You will get an answer as
soon as possible, and credit once it is fixed, if you want it.

What is in scope: `dojo.py`, `dojolib/` and `tools/`, the tutor rules and skills (for example a way to make
the tutor run or reveal something it should not), and the GitHub workflows.

How the repository protects learners: every change to `main` is reviewed by the owner;
`python dojo.py update` shows incoming changes, and which of them run code, before applying
them; personal data (`progress/`, `workspace/`, `exports/`) is gitignored and checked before
every push.
