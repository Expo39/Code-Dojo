from group_anagrams import group_anagrams


def test_example():
    assert group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) == [
        ["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]


def test_empty():
    assert group_anagrams([]) == []


def test_empty_string_and_single():
    assert group_anagrams(["", "a", ""]) == [["", ""], ["a"]]
