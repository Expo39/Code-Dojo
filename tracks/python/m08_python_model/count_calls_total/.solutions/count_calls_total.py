total_calls = 0


def record_call():
    """Add one to the module-level total_calls and return the new value."""
    global total_calls
    total_calls = total_calls + 1
    return total_calls
