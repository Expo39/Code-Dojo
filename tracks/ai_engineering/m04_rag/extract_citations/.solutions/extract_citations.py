import re


def extract_citations(answer, valid_ids):
    valid = set(valid_ids)
    cited, unknown = [], []
    for cid in re.findall(r"\[([A-Za-z0-9_-]+)\]", answer):
        bucket = cited if cid in valid else unknown
        if cid not in bucket:
            bucket.append(cid)
    return {"cited": cited, "unknown": unknown, "abstained": "not in the documents" in answer.lower()}
