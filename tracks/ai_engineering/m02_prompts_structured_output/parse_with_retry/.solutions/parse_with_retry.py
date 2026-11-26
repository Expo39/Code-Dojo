import json


def parse_with_retry(model, prompt, required_keys, max_attempts):
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    for _ in range(max_attempts):
        reply = model(prompt)
        try:
            data = json.loads(reply)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and all(key in data for key in required_keys):
            return data
    raise ValueError(f"no usable JSON with keys {list(required_keys)} after {max_attempts} attempts")
