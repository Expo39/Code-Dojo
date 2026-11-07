def summarise_scores(scores: list[float], pass_mark: float | None = None) -> dict[str, float | None]:
    """Return the mean, best, worst and pass rate of a list of quiz scores.

    The mean and pass rate are rounded to 2 decimals. Every value is None when
    `scores` is empty; the pass rate is also None when no pass mark is given.
    """
    if not scores:
        return {"mean": None, "best": None, "worst": None, "pass_rate": None}
    pass_rate = None
    if pass_mark is not None:
        passed = sum(1 for score in scores if score >= pass_mark)
        pass_rate = round(passed / len(scores), 2)
    return {
        "mean": round(sum(scores) / len(scores), 2),
        "best": max(scores),
        "worst": min(scores),
        "pass_rate": pass_rate,
    }
