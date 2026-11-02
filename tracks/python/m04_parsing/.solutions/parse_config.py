def parse_config(text):
    config = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"bad line: {line!r}")
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        config[key] = int(value) if value.isdigit() else value
    return config
