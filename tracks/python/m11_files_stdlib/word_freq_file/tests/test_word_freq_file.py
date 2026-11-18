import pytest
from word_freq_file import word_freq_file


def test_counts(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text("The cat. the DOG! the cat?", encoding="utf-8")
    assert word_freq_file(f, 2) == [("the", 3), ("cat", 2)]


def test_str_path_and_ties(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text("b a c", encoding="utf-8")
    assert word_freq_file(str(f), 5) == [("a", 1), ("b", 1), ("c", 1)]


def test_unicode(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text("café café thé", encoding="utf-8")
    assert word_freq_file(f, 1) == [("café", 2)]


def test_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        word_freq_file(tmp_path / "nope.txt", 1)
