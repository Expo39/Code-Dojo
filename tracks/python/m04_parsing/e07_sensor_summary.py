"""Summarise sensor readings.

Level: medium
Target: 25

Lines look like "sensor_id,timestamp,value". Return a dict
{sensor_id: {"count": n, "min": x, "max": y, "avg": z}} summarising each sensor.

    "t1,2026-11-02T10:00,20\nt1,2026-11-02T10:05,22\nt2,2026-11-02T10:00,5"
    -> {"t1": {"count": 2, "min": 20.0, "max": 22.0, "avg": 21.0},
        "t2": {"count": 1, "min": 5.0, "max": 5.0, "avg": 5.0}}

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify sensor_summary
"""


def sensor_summary(text):
    raise NotImplementedError
