def top_endpoints(lines, n):
    counts = {}
    for line in lines:
        fields = line.split()
        if len(fields) != 4 or not fields[2].isdigit():
            continue
        _method, path, status, _duration = fields
        if 200 <= int(status) <= 299:
            counts[path] = counts.get(path, 0) + 1
    ranked = sorted(counts.items(), key=lambda pc: (-pc[1], pc[0]))
    return ranked[:n]
