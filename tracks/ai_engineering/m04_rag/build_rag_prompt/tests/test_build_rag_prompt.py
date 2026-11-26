from build_rag_prompt import INSTRUCTION, build_rag_prompt


def passage(pid, text, score):
    return {"id": pid, "text": text, "score": score}


def test_example():
    prompt, used = build_rag_prompt("When is it open?", [passage("p1", "Open 9 to 5.", 0.9)], 10)
    assert used == ["p1"]
    assert prompt == INSTRUCTION + "\n\n[p1] Open 9 to 5.\n\nQuestion: When is it open?\nAnswer:"


def test_best_scores_first_and_a_passage_that_does_not_fit_is_skipped():
    passages = [passage("p1", "a b c", 0.9), passage("p2", "a b c d e", 0.7), passage("p3", "a b", 0.8)]
    prompt, used = build_rag_prompt("q?", passages, 6)
    assert used == ["p1", "p3"]
    assert prompt == INSTRUCTION + "\n\n[p1] a b c\n[p3] a b\n\nQuestion: q?\nAnswer:"


def test_a_later_smaller_passage_can_still_fit_after_a_skip():
    passages = [passage("big", "w " * 8, 0.9), passage("small", "x y", 0.5)]
    _, used = build_rag_prompt("q?", passages, 5)
    assert used == ["small"]


def test_equal_scores_keep_input_order():
    passages = [passage("b", "one", 0.5), passage("a", "two", 0.5)]
    _, used = build_rag_prompt("q?", passages, 10)
    assert used == ["b", "a"]


def test_nothing_fits_leaves_out_the_passage_block():
    prompt, used = build_rag_prompt("q?", [passage("p1", "far too long for this", 0.9)], 2)
    assert used == []
    assert prompt == INSTRUCTION + "\n\nQuestion: q?\nAnswer:"


def test_no_passages():
    prompt, used = build_rag_prompt("q?", [], 100)
    assert used == []
    assert prompt == INSTRUCTION + "\n\nQuestion: q?\nAnswer:"


def test_the_inputs_are_not_changed():
    passages = [passage("p2", "b", 0.1), passage("p1", "a", 0.9)]
    build_rag_prompt("q?", passages, 10)
    assert [p["id"] for p in passages] == ["p2", "p1"]
