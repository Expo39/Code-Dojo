def parse_pairs(text):
    records = []
    for line in text.splitlines():
        tokens = line.split()
        if not tokens:
            continue
        if len(tokens) % 2 != 0:
            raise ValueError(f"odd number of tokens: {line!r}")
        record = {}
        for i in range(0, len(tokens), 2):
            record[tokens[i]] = tokens[i + 1]
        records.append(record)
    return records
