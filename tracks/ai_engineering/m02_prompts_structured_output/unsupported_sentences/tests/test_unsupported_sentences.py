from unsupported_sentences import unsupported_sentences

REFUNDS = ["Refunds are issued within 5 days of the return."]


def test_example():
    answer = "Refunds are issued within 5 days. We also offer free shipping worldwide."
    assert unsupported_sentences(answer, REFUNDS, 0.6) == ["We also offer free shipping worldwide."]


def test_trace_a_number_that_no_passage_contains():
    passages = ["Paris is the capital of France."]
    answer = "Paris is the capital of France. It has 2 million people!"
    assert unsupported_sentences(answer, passages, 0.5) == ["It has 2 million people!"]


def test_exactly_at_the_threshold_is_supported():
    # content words: refunds, takes, 9, days -> two of four are in the passage
    assert unsupported_sentences("Refunds takes 9 days.", REFUNDS, 0.5) == []
    assert unsupported_sentences("Refunds takes 9 days.", REFUNDS, 0.51) == ["Refunds takes 9 days."]


def test_one_passage_must_support_the_sentence_not_the_union():
    passages = ["Alpha beta.", "Gamma delta."]
    assert unsupported_sentences("Alpha delta.", passages, 1.0) == ["Alpha delta."]
    assert unsupported_sentences("Alpha delta.", passages, 0.5) == []


def test_case_and_punctuation_do_not_matter():
    assert unsupported_sentences("REFUNDS, issued: within 5 DAYS!", REFUNDS, 1.0) == []


def test_a_sentence_of_only_stopwords_is_supported():
    assert unsupported_sentences("It is the.", REFUNDS, 1.0) == []


def test_several_unsupported_sentences_keep_their_order_and_marks():
    answer = "Nothing here? Still nothing! Refunds are issued."
    assert unsupported_sentences(answer, REFUNDS, 0.5) == ["Nothing here?", "Still nothing!"]


def test_empty_answer_or_no_passages():
    assert unsupported_sentences("", REFUNDS, 0.5) == []
    assert unsupported_sentences("Something.", [], 0.5) == ["Something."]
