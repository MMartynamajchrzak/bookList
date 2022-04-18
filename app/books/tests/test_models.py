from django.core.exceptions import ValidationError
from django.test import TestCase

from .conftest import book, sample_book


class TestBookModel(TestCase):

    def setUp(self) -> None:
        self.created_book = sample_book()

    def test_create_book(self) -> None:
        self.assertEqual(self.created_book.author, book['author'])
        self.assertEqual(self.created_book.published_date, book['published_date'])
        self.assertEqual(self.created_book.cover_link, book['cover_link'])

    def test_str_book(self) -> None:
        self.assertEqual(str(self.created_book), f'{self.created_book.title}, {self.created_book.author}')

    def test_isbn_must_be_13_or_10_digit(self) -> None:
        self.created_book.full_clean()
        self.created_book.ISBN = '12345'
        self.assertRaises(ValidationError, self.created_book.full_clean)

    def test_validate_book_url(self) -> None:
        self.created_book.full_clean()
        self.created_book.cover_link = 'not url'
        self.assertRaises(ValidationError, self.created_book.full_clean)
