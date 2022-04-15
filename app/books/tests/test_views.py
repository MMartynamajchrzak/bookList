from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from .conftest import sample_book, book


class TestAddUpdateBookFormView(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_add_book_redirects_successfully(self):
        resp = self.client.post(reverse('add_book'), data=book, follow=True)

        self.assertRedirects(resp, reverse('list_books'), status_code=302, target_status_code=200)
        self.assertEqual(len(Book.objects.all()), 1)


    def test_update_book_redirects_successfully(self):
        created_book = sample_book()

        updated_book = {
            'title': 'Updated Title',
            'author': 'Test Author',
            'pages_count': 123,
            'language': 'Polish'
        }

        resp = self.client.post(reverse('update_book', kwargs={'pk': created_book.id}), data=updated_book, follow=True)
        created_book.refresh_from_db()

        self.assertRedirects(resp, reverse('list_books'), status_code=302, target_status_code=200)
        self.assertEqual(created_book.title, updated_book['title'])


class TestBookViewSet(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_all_users_successful(self):
        created_book = sample_book()
        resp = self.client.get(reverse('all'))
        print(resp.data['results'][0]['title'])

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(created_book.title, resp.data['results'][0]['title'])
        self.assertEqual(created_book.cover_link, resp.data['results'][0]['cover_link'])
        self.assertEqual(created_book.published_date, resp.data['results'][0]['published_date'])
        self.assertEqual(len(resp.data['results']), 1)
