import environ
import requests
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .filters import BookRestFilter, BookFilter
from .models import Book
from .serializers import BookSerializer

env = environ.Env()


class BaseBookFormView:
    model = Book
    template_name = 'form.html'
    fields = ['title', 'author', 'published_date', 'ISBN', 'pages_count', 'cover_link', 'language']
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
    pass


class UpdateBookFormView(BaseBookFormView, UpdateView):
    pass


"""PART 2 Add books from external api"""
class ImportBookViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = []
    authentication_classes = []

    """external api call to get books data by accessing specific query params"""
    @staticmethod
    def get_books_from_external_api(_params: str) -> list:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={_params}"
                                f"&key={env.str('EXTERNAL_API_KEY', default='')}")
        response.raise_for_status()

        return response.json()['items']


    def create(self, request, *args, params, **kwargs):

        # parsing books
        def _parse_book(_api):
            return {
                'title': _api['volumeInfo']['title'],
                'author': _api['volumeInfo']['authors'][0],
                'published_date': _api['volumeInfo']['publishedDate'],
                'ISBN': _api['volumeInfo']['industryIdentifiers'][1]['identifier'],
                'page_count': _api['volumeInfo']['pageCount'],
                'cover_link': _api['volumeInfo']['previewLink'],
                'language': _api['volumeInfo']['language']
            }

        google_api_results = self.get_books_from_external_api(params)

        # create list of books from api where the date format is correct
        book_data = [_parse_book(google_api_results[i]) for i in range(len(google_api_results))
                         if len(google_api_results[i]['volumeInfo']['publishedDate']) == 10]

        # serialize and save to db
        s_books = BookSerializer(data=book_data, many=True, context={'request': request})
        s_books.is_valid(raise_exception=True)
        s_books.save()


        return Response(data=s_books.data, status=status.HTTP_201_CREATED)


"""PART 3 List all books, with filtering by query params from django filters"""
class BookListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookRestFilter
