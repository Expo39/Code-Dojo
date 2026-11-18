import types
from read_chunks import read_chunks


def test_example():
    assert list(read_chunks(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_is_generator():
    assert isinstance(read_chunks([1], 1), types.GeneratorType)


def test_one_shot_iterator():
    it = iter([1, 2, 3])
    assert list(read_chunks(it, 2)) == [[1, 2], [3]]


def test_empty():
    assert list(read_chunks([], 3)) == []
