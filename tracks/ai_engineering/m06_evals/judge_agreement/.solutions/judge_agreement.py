def judge_agreement(human, judge):
    if len(human) != len(judge):
        raise ValueError("human and judge must have the same length")
    pairs = list(zip(human, judge))
    agree = sum(1 for h, j in pairs if h == j)
    return {
        "agreement": agree / len(pairs) if pairs else 0.0,
        "false_pass": sum(1 for h, j in pairs if j == "pass" and h == "fail"),
        "false_fail": sum(1 for h, j in pairs if j == "fail" and h == "pass"),
    }
