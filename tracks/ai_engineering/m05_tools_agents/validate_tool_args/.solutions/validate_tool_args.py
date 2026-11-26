TYPES = {"str": str, "int": int, "float": (int, float), "bool": bool}


def validate_tool_args(schema, args):
    errors = []
    for name, spec in schema.items():
        if name not in args:
            if spec.get("required", False):
                errors.append(f"missing required argument '{name}'")
            continue
        value = args[name]
        expected = spec["type"]
        ok = isinstance(value, TYPES[expected])
        if expected in ("int", "float") and isinstance(value, bool):
            ok = False
        if not ok:
            errors.append(f"argument '{name}' must be {expected}, got {type(value).__name__}")
    for name in args:
        if name not in schema:
            errors.append(f"unknown argument '{name}'")
    return errors
