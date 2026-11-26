import pytest
from chunk_words import chunk_words


def test_example():
    assert chunk_words("a b c d e f g", 4, 1) == ["a b c d", "d e f g"]


def test_overlap_two_with_a_short_last_chunk():
    text = "one two three four five six seven eight nine"
    assert chunk_words(text, 4, 2) == [
        "one two three four", "three four five six", "five six seven eight", "seven eight nine"]


def test_no_overlap():
    assert chunk_words("a b c d e", 2, 0) == ["a b", "c d", "e"]


def test_no_chunk_that_only_repeats_words():
    assert chunk_words("a b c d e f", 3, 1) == ["a b c", "c d e", "e f"]
    assert chunk_words("a b c d e", 3, 1) == ["a b c", "c d e"]


def test_text_shorter_than_size_is_one_chunk():
    assert chunk_words("only three words", 10, 2) == ["only three words"]


def test_whitespace_is_normalised_and_empty_text_gives_no_chunks():
    assert chunk_words("  a   b\nc  ", 2, 0) == ["a b", "c"]
    assert chunk_words("   ", 3, 1) == []
    assert chunk_words("", 3, 1) == []


@pytest.mark.parametrize("size, overlap", [(0, 0), (3, 3), (3, 4), (3, -1)])
def test_invalid_sizes_raise(size, overlap):
    with pytest.raises(ValueError):
        chunk_words("a b c d", size, overlap)
