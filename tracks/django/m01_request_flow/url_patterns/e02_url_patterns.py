"""Map URLs to views, and back.

Level: easy
Target: 15

The three views below exist already. Write `urlpatterns` (the list Django reads) so that:

| URL | view | name |
| --- | --- | --- |
| `/` | `home` | `home` |
| `/articles/<number>/` | `article_detail` (argument `pk`, an integer) | `article-detail` |
| `/archive/<year>/<slug>/` | `archive` (arguments `year`, an integer, and `slug`) | `archive` |

- Use path converters so that `/articles/abc/` does not match any pattern at all (Django
  answers 404 before any view runs), and so that `pk` and `year` arrive as integers.
- Every pattern has the name in the table, so code can build URLs with `reverse(name, ...)`
  instead of writing paths by hand.

    reverse("article-detail", kwargs={"pk": 7})   -> "/articles/7/"

Trace by hand (the result or the error):

    resolve("/archive/2026/autumn-news/").kwargs                    -> ?
    reverse("archive", kwargs={"year": 2026, "slug": "autumn-news"}) -> ?
    resolve("/articles/7a/")                                         -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify url_patterns
"""

from django.http import HttpResponse
from django.urls import path


def home(request):
    return HttpResponse("home")


def article_detail(request, pk):
    return HttpResponse(f"article {pk}")


def archive(request, year, slug):
    return HttpResponse(f"archive {year} {slug}")


urlpatterns = []
