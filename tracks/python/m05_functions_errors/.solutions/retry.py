def retry(func, attempts):
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    last_error = None
    for _ in range(attempts):
        try:
            return func()
        except Exception as error:
            last_error = error
    raise last_error
