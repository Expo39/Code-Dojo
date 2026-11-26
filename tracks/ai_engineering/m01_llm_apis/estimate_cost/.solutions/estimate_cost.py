def estimate_cost(model, input_tokens, output_tokens, cache_read_tokens, prices):
    if model not in prices:
        raise ValueError(f"unknown model: {model!r}")
    counts = {"input": input_tokens, "output": output_tokens, "cache_read": cache_read_tokens}
    if any(count < 0 for count in counts.values()):
        raise ValueError("token counts cannot be negative")
    rates = prices[model]
    total = sum(count * rates[kind] for kind, count in counts.items()) / 1_000_000
    return round(total, 2)
