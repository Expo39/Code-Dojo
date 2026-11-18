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

Trace by hand (work out the result yourself):

    2026-11-05 09:00:00 user=dan ERROR crash
    2026-11-05 09:01:00 WARN user=eve slow
    2026-11-05 09:02:00 ERROR user=eve oops
    2026-11-05 09:03:00 user=dan INFO restart
    -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify errors_by_user
"""


def errors_by_user(log_text):
    raise NotImplementedError
