def errors_by_user(log_text):
    counts = {}
    for line in log_text.splitlines():
        level = None
        user = None
        for token in line.split():
            if token in ("INFO", "WARN", "ERROR"):
                level = token
            elif token.startswith("user="):
                user = token[len("user="):]
        if level == "ERROR" and user:
            counts[user] = counts.get(user, 0) + 1
    return counts
