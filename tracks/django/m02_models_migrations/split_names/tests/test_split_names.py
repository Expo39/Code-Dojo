import pytest
from django.db import models
from split_names import split_names


class SplitPerson(models.Model):
    full_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        app_label = "dojo"


pytestmark = pytest.mark.django_db


def people(*names, first=""):
    return [SplitPerson.objects.create(full_name=n, first_name=first) for n in names]


def names(person):
    person.refresh_from_db()
    return person.first_name, person.last_name


def test_two_words_and_one_word_and_many_words():
    ada, cher, mary = people("Ada Lovelace", "Cher", "Mary Ann Smith")
    assert split_names(SplitPerson) == 3
    assert names(ada) == ("Ada", "Lovelace")
    assert names(cher) == ("Cher", "")
    assert names(mary) == ("Mary Ann", "Smith")


def test_trace_with_spaces_and_an_empty_name():
    alan, plato, empty, grace = people("  Alan   Turing ", "Plato", "", "Grace Brewster Murray Hopper")
    assert split_names(SplitPerson) == 3
    assert names(alan) == ("Alan", "Turing")
    assert names(plato) == ("Plato", "")
    assert names(empty) == ("", "")
    assert names(grace) == ("Grace Brewster Murray", "Hopper")


def test_running_twice_changes_nobody_the_second_time():
    people("Ada Lovelace")
    assert split_names(SplitPerson) == 1
    assert split_names(SplitPerson) == 0


def test_people_who_already_have_a_first_name_are_left_alone():
    (done,) = people("Ada Lovelace", first="Augusta")
    assert split_names(SplitPerson) == 0
    assert names(done) == ("Augusta", "")


def test_a_name_of_only_spaces_is_ignored():
    (blank,) = people("   ")
    assert split_names(SplitPerson) == 0
    assert names(blank) == ("", "")


def test_no_people():
    assert split_names(SplitPerson) == 0


def test_at_most_two_queries_for_many_people(django_assert_max_num_queries):
    people(*[f"First{i} Last{i}" for i in range(30)])
    with django_assert_max_num_queries(2):
        assert split_names(SplitPerson) == 30
