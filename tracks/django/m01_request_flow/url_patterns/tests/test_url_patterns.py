import pytest
import url_patterns
from django.test import override_settings
from django.urls import Resolver404, resolve, reverse

pytestmark = pytest.mark.urls("url_patterns")


def test_home():
    assert reverse("home") == "/"
    assert resolve("/").func is url_patterns.home


def test_article_detail_builds_and_resolves_with_an_integer():
    assert reverse("article-detail", kwargs={"pk": 7}) == "/articles/7/"
    match = resolve("/articles/7/")
    assert match.func is url_patterns.article_detail
    assert match.kwargs == {"pk": 7} and isinstance(match.kwargs["pk"], int)


def test_a_non_integer_pk_matches_nothing():
    for url in ("/articles/abc/", "/articles/7a/", "/articles/-1/", "/articles//"):
        with pytest.raises(Resolver404):
            resolve(url)


def test_archive_converts_the_year_and_keeps_the_slug():
    match = resolve("/archive/2026/autumn-news/")
    assert match.func is url_patterns.archive
    assert match.kwargs == {"year": 2026, "slug": "autumn-news"}
    assert reverse("archive", kwargs={"year": 2026, "slug": "autumn-news"}) == "/archive/2026/autumn-news/"


def test_a_slug_with_spaces_or_a_text_year_does_not_match():
    with pytest.raises(Resolver404):
        resolve("/archive/2026/autumn news/")
    with pytest.raises(Resolver404):
        resolve("/archive/year/autumn-news/")


def test_the_test_client_reaches_the_views(client):
    assert client.get("/articles/12/").content == b"article 12"
    assert client.get("/articles/x/").status_code == 404
