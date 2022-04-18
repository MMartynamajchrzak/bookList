from django.test import TestCase

from books.forms import BookForm, GoogleSearchForm
from .conftest import book


class TestBookForm(TestCase):

    def setUp(self) -> None:
        self.form_data = {
            'title': book['title'],
            'author': book['author'],
            'language': book['language']
        }

    def test_fields_required_passed(self) -> None:
        form = BookForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_fields_required_failed(self) -> None:
        del self.form_data['author']
        form = BookForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_date_format_failed(self) -> None:
        self.form_data['published_date'] = '2020'
        form = BookForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_url_format_failed(self) -> None:
        self.form_data['cover_link'] = 'no url'
        form = BookForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestGoogleSearchForm(TestCase):

    def test_no_fields_required(self) -> None:
        form_data = {}

        form = GoogleSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
