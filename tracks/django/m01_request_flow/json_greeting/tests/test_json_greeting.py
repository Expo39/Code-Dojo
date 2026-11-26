import json

from django.test import RequestFactory
from json_greeting import greeting

rf = RequestFactory()


def body(response):
    return json.loads(response.content)


def test_name_from_the_query_string():
    response = greeting(rf.get("/", {"name": "Ada"}))
    assert response.status_code == 200
    assert body(response) == {"message": "Hello, Ada!"}


def test_missing_name_uses_world():
    assert body(greeting(rf.get("/"))) == {"message": "Hello, world!"}


def test_blank_name_uses_world():
    assert body(greeting(rf.get("/", {"name": "   "}))) == {"message": "Hello, world!"}
    assert body(greeting(rf.get("/", {"name": ""}))) == {"message": "Hello, world!"}


def test_surrounding_spaces_are_removed_but_inner_spaces_stay():
    response = greeting(rf.get("/", {"name": "  Grace Hopper "}))
    assert body(response) == {"message": "Hello, Grace Hopper!"}


def test_the_response_is_json():
    assert greeting(rf.get("/")).headers["Content-Type"].startswith("application/json")


def test_other_methods_get_405_and_an_allow_header():
    for method in (rf.post, rf.put, rf.delete):
        response = greeting(method("/"))
        assert response.status_code == 405
        assert response.headers["Allow"] == "GET"


def test_non_ascii_names_survive():
    assert body(greeting(rf.get("/", {"name": "Zoë"}))) == {"message": "Hello, Zoë!"}
