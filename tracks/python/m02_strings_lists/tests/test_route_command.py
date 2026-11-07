from route_command import route_command


def test_each_command():
    assert route_command("go north") == "You walk north."
    assert route_command("take lamp") == "You take the lamp."
    assert route_command("look") == "You look around."
    assert route_command("quit") == "Goodbye."


def test_multi_word_item():
    assert route_command("take rusty key") == "You take the rusty key."


def test_case_and_spaces():
    assert route_command("  GO   East ") == "You walk east."


def test_wrong_number_of_words():
    assert route_command("go") == "I don't understand that."
    assert route_command("take") == "I don't understand that."
    assert route_command("go north east") == "I don't understand that."
    assert route_command("look around") == "I don't understand that."


def test_unknown_and_empty():
    assert route_command("dance") == "I don't understand that."
    assert route_command("") == "I don't understand that."
