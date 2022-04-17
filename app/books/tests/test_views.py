from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from django_filters import CharFilter, DateFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.views import BookListViewSet
from .conftest import sample_book, book, mock_google_api


"""test list book view"""
class TestBookListView(TestCase):

    def test_url_exists(self) -> None:
        response = self.client.get("/books/list/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('list_books'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('list_books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_pagination_is_correct(self) -> None:
        # create 30 books to check whether 20 will be displayed
        for _ in range(30):
            sample_book()

        response = self.client.get(reverse('list_books'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('is_paginated', response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['book_list']), 10)


"""Test add book form"""
class TestAddBookFormView(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_url_add_exists(self) -> None:
        response = self.client.get("/books/add/")
        self.assertEqual(response.status_code, 200)

    def test_url_add_accessible_by_name(self) -> None:
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)

    def test_add_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_add_book_redirects_successfully(self) -> None:
        resp = self.client.post(reverse('add_book'), data=book, follow=True)

        book_obj_str = resp.context[0]['object_list'][0]
        book_obj_str = str(book_obj_str).split(',')[0]

        self.assertRedirects(resp, reverse('list_books'), status_code=302, target_status_code=200)
        self.assertEqual(len(Book.objects.all()), 1)
        self.assertEqual(book['title'], book_obj_str)


"""Test update book form"""
class TestUpdateBookFormView(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.created_book = sample_book()

    def test_url_update_exists(self) -> None:
        response = self.client.get(f"/books/update/{self.created_book.id}/")
        self.assertEqual(response.status_code, 200)

    def test_url_update_accessible_by_name(self) -> None:
        response = self.client.post(reverse('update_book', kwargs={'pk': self.created_book.id}))
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('update_book', kwargs={'pk': self.created_book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_update_book_redirects_successfully(self) -> None:
        updated_book = {
            'title': 'Updated Title',
            'author': 'Test Author',
            'pages_count': 123,
            'language': 'Polish'
        }

        resp = self.client.post(reverse('update_book', kwargs={'pk': self.created_book.id}), data=updated_book, follow=True)
        self.created_book.refresh_from_db()

        self.assertRedirects(resp, reverse('list_books'), status_code=302, target_status_code=200)
        self.assertEqual(self.created_book.title, updated_book['title'])


"""Test form for importing books"""
class TestImportBooksForm(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    @patch('books.views.ImportBookFormView.get_books_from_external_api')
    def test_import_books_by_field_contains(self, mock_get_books_from_external_api) -> None:

        mock_get_books_from_external_api.return_value = mock_google_api()
        resp = self.client.post(reverse('import_books'), data={'title': 'Witcher'})


        self.assertRedirects(resp, reverse('list_books'), status_code=302, target_status_code=200)
        self.assertEqual(len(Book.objects.all()), 1)
        self.assertEqual(Book.objects.first().title, mock_google_api()[0]['volumeInfo']['title'])


"""Test Book ViewSet"""
class TestBookViewSet(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_all_users_successful(self) -> None:
        created_book = sample_book()
        resp = self.client.get(reverse('all'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(created_book.title, resp.data['results'][0]['title'])
        self.assertEqual(created_book.cover_link, resp.data['results'][0]['cover_link'])
        self.assertEqual(created_book.published_date, resp.data['results'][0]['published_date'])
        self.assertEqual(len(resp.data['results']), 1)

    """test filters"""
    def test_filterset_class(self) -> None:

        class Filter(FilterSet):
            class Meta:
                model = Book
                fields = ['title', 'author', 'language']

        backend = DjangoFilterBackend()
        view = BookListViewSet()
        view.filterset_class = Filter
        queryset = Book.objects.all()

        filterset_class = backend.get_filterset_class(view, queryset)
        self.assertIs(filterset_class, Filter)

    def test_filterset_fields(self) -> None:

        backend = DjangoFilterBackend()
        view = BookListViewSet()

        view.filterset_fields = {
            'title': ['icontains'],
            'author': ['icontains'],
            'language': ['exact']
        }
        queryset = Book.objects.all()

        filterset_class = backend.get_filterset_class(view, queryset)
        self.assertEqual(filterset_class._meta.fields, view.filterset_fields)


    @override_settings(FILTERS_DEFAULT_LOOKUP_EXPR='icontains')
    def test_modified_default_lookup(self) -> None:

        f = Book._meta.get_field('title')
        f2 = Book._meta.get_field('author')
        result = FilterSet.filter_for_field(f, 'title')
        result_2 = FilterSet.filter_for_field(f2, 'author')

        self.assertIsInstance(result, CharFilter)
        self.assertEqual(result.lookup_expr, 'icontains')
        self.assertEqual(result_2.lookup_expr, 'icontains')


    @override_settings(FILTERS_DEFAULT_LOOKUP_EXPR='exact')
    def test_modified_default_lookup(self) -> None:
        f = Book._meta.get_field('language')
        result = FilterSet.filter_for_field(f, 'language')

        self.assertIsInstance(result, CharFilter)
        self.assertEqual(result.lookup_expr, 'exact')


    @override_settings(FILTERS_DEFAULT_LOOKUP_EXPR='lte')
    def test_modified_default_lookup(self) -> None:
        f = Book._meta.get_field('published_date')
        result = FilterSet.filter_for_field(f, 'to_date')

        self.assertIsInstance(result, DateFilter)
        self.assertEqual(result.lookup_expr, 'lte')


    @override_settings(FILTERS_DEFAULT_LOOKUP_EXPR='gte')
    def test_modified_default_lookup(self) -> None:
        f = Book._meta.get_field('published_date')
        result = FilterSet.filter_for_field(f, 'from_date')

        self.assertIsInstance(result, DateFilter)
        self.assertEqual(result.lookup_expr, 'gte')
