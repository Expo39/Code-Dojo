def sensor_summary(text):
    values = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split(",")
        if len(parts) != 3:
            continue
        sensor, _timestamp, raw = (p.strip() for p in parts)
        try:
            value = float(raw)
        except ValueError:
            continue
        values.setdefault(sensor, []).append(value)
    return {
        sensor: {
            "count": len(vals),
            "min": min(vals),
            "max": max(vals),
            "avg": round(sum(vals) / len(vals), 2),
        }
        for sensor, vals in values.items()
    }
