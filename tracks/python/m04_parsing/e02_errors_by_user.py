"""Count ERROR lines per user.

Level: easy
Target: 15
Pattern: parse-then-act

(A real live-coding interview question.)

Each log line has space-separated tokens. One token is the level (INFO, WARN,
ERROR); somewhere else, before or after it, is a token user=<name>. Tokens can
come in any order. Return a dict {user: number of ERROR lines}. Ignore lines
with no user.

    2026-10-23 10:00:01 ERROR user=alice disk full
    2026-10-23 10:00:02 user=bob INFO login
    2026-10-23 10:00:03 user=alice ERROR timeout
    -> {"alice": 2}

Tip: parse the WHOLE line into variables first (level, user), then decide.
"""


def errors_by_user(log_text):
    raise NotImplementedError
