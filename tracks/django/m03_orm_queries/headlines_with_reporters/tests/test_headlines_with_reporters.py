import pytest
from django.db import models
from headlines_with_reporters import headlines_with_reporters


class Reporter(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = "dojo"


class Story(models.Model):
    headline = models.CharField(max_length=80)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, related_name="stories")

    class Meta:
        app_label = "dojo"


pytestmark = pytest.mark.django_db


def seed(*pairs):
    reporters = {}
    for headline, name in pairs:
        reporter = reporters.setdefault(name, Reporter.objects.create(name=name))
        Story.objects.create(headline=headline, reporter=reporter)


def test_example():
    seed(("Floods", "Ada"), ("Budget", "Bo"))
    assert headlines_with_reporters(Story) == ["Budget - Bo", "Floods - Ada"]


def test_trace():
    seed(("Zoo opens", "Cy"), ("Art fair", "Cy"), ("Marathon", "Di"))
    assert headlines_with_reporters(Story) == ["Art fair - Cy", "Marathon - Di", "Zoo opens - Cy"]


def test_empty():
    assert headlines_with_reporters(Story) == []


def test_exactly_one_query_for_many_stories(django_assert_num_queries):
    seed(*[(f"Story {i:02d}", f"Reporter {i % 7}") for i in range(40)])
    with django_assert_num_queries(1):
        result = headlines_with_reporters(Story)
    assert len(result) == 40 and result[0] == "Story 00 - Reporter 0"


def test_returns_a_list_of_strings():
    seed(("A", "x"))
    result = headlines_with_reporters(Story)
    assert isinstance(result, list) and all(isinstance(s, str) for s in result)
