"""Count ERROR lines per user.

Level: easy
Target: 15

(A real live-coding interview question.)

Each log line has space-separated tokens, among them a level (INFO, WARN or
ERROR) and a token user=<name>. Return a dict {user: number of ERROR lines}.

    2026-10-23 10:00:01 ERROR user=alice disk full
    2026-10-23 10:00:02 user=bob INFO login
    2026-10-23 10:00:03 user=alice ERROR timeout
    -> {"alice": 2}

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify errors_by_user
"""


def errors_by_user(log_text):
    raise NotImplementedError
