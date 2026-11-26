import re

from django.http import HttpResponse
from django.test import RequestFactory
from request_id_middleware import RequestIDMiddleware

rf = RequestFactory()


def run(**extra):
    seen = {}

    def get_response(request):
        seen["id"] = request.request_id
        return HttpResponse("ok")

    response = RequestIDMiddleware(get_response)(rf.get("/", **extra))
    return seen["id"], response


def test_a_good_incoming_id_is_kept():
    request_id, response = run(HTTP_X_REQUEST_ID="abc-123")
    assert request_id == "abc-123"
    assert response["X-Request-ID"] == "abc-123"


def test_the_id_is_set_before_the_view_runs():
    request_id, _ = run(HTTP_X_REQUEST_ID="early_1")
    assert request_id == "early_1"


def test_a_missing_header_gets_a_new_hex_id_each_time():
    first, response = run()
    second, _ = run()
    assert re.fullmatch(r"[0-9a-f]{32}", first)
    assert first != second
    assert response["X-Request-ID"] == first


def test_surrounding_spaces_are_stripped_and_the_stripped_value_is_kept():
    request_id, response = run(HTTP_X_REQUEST_ID="  req_9  ")
    assert request_id == "req_9" and response["X-Request-ID"] == "req_9"


def test_unsafe_or_overlong_ids_are_replaced():
    for bad in ("has space", "semi;colon", "new\nline", "x" * 65, "ünï"):
        request_id, response = run(HTTP_X_REQUEST_ID=bad)
        assert re.fullmatch(r"[0-9a-f]{32}", request_id), bad
        assert response["X-Request-ID"] == request_id


def test_exactly_64_characters_is_allowed():
    assert run(HTTP_X_REQUEST_ID="a" * 64)[0] == "a" * 64


def test_an_empty_or_blank_header_is_replaced():
    for blank in ("", "   "):
        assert re.fullmatch(r"[0-9a-f]{32}", run(HTTP_X_REQUEST_ID=blank)[0])


def test_the_view_response_is_returned_unchanged_apart_from_the_header():
    _, response = run()
    assert response.content == b"ok" and response.status_code == 200
