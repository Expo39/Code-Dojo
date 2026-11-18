from word_count import word_count


def test_example():
    assert word_count("The cat and the hat.") == {"the": 2, "cat": 1, "and": 1, "hat": 1}


def test_empty():
    assert word_count("") == {}


def test_punctuation_and_case():
    assert word_count("Hi! hi? HI,") == {"hi": 3}
