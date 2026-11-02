from make_grid import make_grid


def test_shape():
    assert make_grid(2, 3) == [[0, 0, 0], [0, 0, 0]]


def test_rows_independent():
    grid = make_grid(3, 2)
    grid[0][0] = 9
    assert grid == [[9, 0], [0, 0], [0, 0]]
