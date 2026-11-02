def parse_csv(text):
    header = None
    rows = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        fields = [f.strip() for f in line.split(",")]
        if header is None:
            header = fields
            continue
        if len(fields) != len(header):
            raise ValueError(f"line {number}: expected {len(header)} fields, got {len(fields)}")
        rows.append(dict(zip(header, fields)))
    return rows
