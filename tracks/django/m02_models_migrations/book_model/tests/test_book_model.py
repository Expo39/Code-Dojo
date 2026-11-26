from decimal import Decimal

import pytest
from book_model import Book
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

pytestmark = pytest.mark.django_db


def make(**overrides):
    values = {"title": "Dune", "isbn": "9780441013593", "pages": 412, "price": Decimal("9.99")}
    return Book.objects.create(**{**values, **overrides})


def test_str_and_is_long():
    book = make()
    assert str(book) == "Dune (9780441013593)"
    assert book.is_long() is False
    assert make(isbn="2", pages=500).is_long() is True
    assert make(isbn="3", pages=499).is_long() is False


def test_books_are_ordered_by_title_by_default():
    make(title="Brave", isbn="1")
    make(title="Alpha", isbn="2")
    make(title="Cedar", isbn="3")
    assert [b.title for b in Book.objects.all()] == ["Alpha", "Brave", "Cedar"]


def test_isbn_is_unique_in_the_database():
    make()
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            make(title="Other")


def test_the_database_refuses_zero_pages():
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            make(pages=0)
    assert make(isbn="9", pages=1).pages == 1


def test_published_is_optional():
    book = make()
    assert book.published is None
    book.full_clean()  # no ValidationError: empty is allowed in forms too


def test_title_is_required_by_validation():
    with pytest.raises(ValidationError):
        Book(title="", isbn="1", pages=10, price=Decimal("1.00")).full_clean()


def test_price_allows_four_digits_before_the_point_and_two_after():
    Book(title="A", isbn="1", pages=10, price=Decimal("9999.99")).full_clean()
    with pytest.raises(ValidationError):
        Book(title="A", isbn="1", pages=10, price=Decimal("10000.00")).full_clean()
    with pytest.raises(ValidationError):
        Book(title="A", isbn="1", pages=10, price=Decimal("1.999")).full_clean()


def test_title_longer_than_200_is_invalid():
    with pytest.raises(ValidationError):
        Book(title="x" * 201, isbn="1", pages=10, price=Decimal("1.00")).full_clean()
