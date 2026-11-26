import pytest
from busiest_authors import busiest_authors
from django.db import models


class Writer(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = "dojo"


class Novel(models.Model):
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name="novels")

    class Meta:
        app_label = "dojo"


pytestmark = pytest.mark.django_db


def seed(**counts):
    for name, n in counts.items():
        writer = Writer.objects.create(name=name)
        for i in range(n):
            Novel.objects.create(title=f"{name}-{i}", writer=writer)


def test_example():
    seed(Ada=3, Bo=1, Cy=3, Di=0)
    assert busiest_authors(Writer, 1, 10) == [("Ada", 3), ("Cy", 3), ("Bo", 1)]


def test_trace_with_min_and_limit():
    seed(Eve=2, Fay=5, Gus=2, Hal=4)
    assert busiest_authors(Writer, 2, 3) == [("Fay", 5), ("Hal", 4), ("Eve", 2)]


def test_writers_with_no_novels_appear_only_when_min_is_zero():
    seed(Ada=1, Di=0)
    assert busiest_authors(Writer, 0, 10) == [("Ada", 1), ("Di", 0)]
    assert busiest_authors(Writer, 1, 10) == [("Ada", 1)]


def test_limit_zero_or_negative_is_empty():
    seed(Ada=2)
    assert busiest_authors(Writer, 0, 0) == []
    assert busiest_authors(Writer, 0, -3) == []


def test_it_returns_tuples_in_a_list():
    seed(Ada=2)
    result = busiest_authors(Writer, 1, 5)
    assert isinstance(result, list) and result == [("Ada", 2)]


def test_one_query_for_any_number_of_writers(django_assert_num_queries):
    seed(**{f"W{i:02d}": i % 4 for i in range(25)})
    with django_assert_num_queries(1):
        busiest_authors(Writer, 1, 100)
