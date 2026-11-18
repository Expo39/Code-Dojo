def make_grid(rows, cols, fill=0):
    """Return a rows x cols list of lists, every cell set to fill."""
    return [[fill] * cols for _ in range(rows)]
