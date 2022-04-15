from django.test import TestCase

from books.serializers import BookSerializer
from .conftest import sample_book


class TestBookSerializer(TestCase):
    def setUp(self) -> None:
        self.book = sample_book()

    def test_serializer_data(self):
        serializer = BookSerializer(self.book)
        data = serializer.data

        self.assertEqual(data['author'], self.book.author)
        self.assertEqual(data['cover_link'], self.book.cover_link)
        self.assertEqual(data['published_date'], self.book.published_date)
