"""Summarise sensor readings.

Level: medium
Target: 25
Pattern: parse-group-aggregate

Lines look like "sensor_id,timestamp,value", e.g. "t1,2026-11-02T10:00,21.5".
Return a dict {sensor_id: {"count": n, "min": x, "max": y, "avg": z}} with avg
rounded to 2 decimals. Skip blank lines and lines whose value is not a number.

    "t1,2026-11-02T10:00,20\nt1,2026-11-02T10:05,22\nt2,2026-11-02T10:00,5"
    -> {"t1": {"count": 2, "min": 20.0, "max": 22.0, "avg": 21.0},
        "t2": {"count": 1, "min": 5.0, "max": 5.0, "avg": 5.0}}
"""


def sensor_summary(text):
    raise NotImplementedError
