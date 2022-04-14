import environ
import requests
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins

from .filters import BookRestFilter, BookFilter
from .forms import BookForm, GoogleSearchForm
from .models import Book
from .serializers import BookSerializer

env = environ.Env()


class BaseBookFormView:
    model = Book
    template_name = 'form.html'
    success_url = reverse_lazy('list_books')


"""PART 1: List, Create, Update"""
class BookListView(ListView):
    model = Book
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())

        return context


class AddBookFormView(BaseBookFormView, CreateView):
    form_class = BookForm


class UpdateBookFormView(BaseBookFormView, UpdateView):
    form_class = BookForm


"""PART 2 Add books from external api"""
class ImportBookFormView(BaseBookFormView, CreateView):
    form_class = GoogleSearchForm
    template_name = 'google_form.html'
    success_url = reverse_lazy('list_books')


    @staticmethod
    def get_books_from_external_api(_params: str) -> list:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={_params}"
                                f"&key={env.str('EXTERNAL_API_KEY', default='')}")
        response.raise_for_status()

        return response.json()['items']


    def post(self, request, *args, **kwargs):

        def _parse_book(_api):
            # special validation from disabled data
            necessary_keys = ['title', 'authors', 'language']
            optional_keys = ['publishedDate', 'pageCount', 'previewLink', 'industryIdentifiers']

            for key in necessary_keys:
                if not key in _api['volumeInfo']:
                    continue

            for key in optional_keys:
                if not key in _api['volumeInfo'] or (key == optional_keys[0] and len(_api['volumeInfo'][key]) != 10):
                    _api['volumeInfo'][key] = None

            return {
                'title': _api['volumeInfo']['title'],
                'author': _api['volumeInfo']['authors'][0],
                'published_date': _api['volumeInfo']['publishedDate'],
                'ISBN': _api['volumeInfo']['industryIdentifiers'][1]['identifier'],
                'pages_count': _api['volumeInfo']['pageCount'],
                'cover_link': _api['volumeInfo']['previewLink'],
                'language': _api['volumeInfo']['language']
            }

        params = ''
        title = self.request.POST.get('title')
        author = self.request.POST.get('author')
        isbn = self.request.POST.get('ISBN')

        if title:
            params = f'intitle:{title}+'
        if author:
            params += f'inauthor:{author}+'
        if isbn:
            params += f'isbn:{isbn}+'

        google_api_results = self.get_books_from_external_api(params)

        # create list of books from api where the date format is correct
        book_data = [_parse_book(google_api_results[i]) for i in range(len(google_api_results))]

        # serialize and save to db
        s_books = BookSerializer(data=book_data, many=True)
        s_books.is_valid(raise_exception=True)
        s_books.save()


        return redirect('list_books')


"""PART 3 List all books, with filtering by query params from django filters"""
class BookListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookRestFilter
