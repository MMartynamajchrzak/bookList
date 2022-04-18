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
from .parsers import _parse_book
from .serializers import BookSerializer

env = environ.Env()


# base book form used to create AddBookFormView and UpdateFormView
class BaseBookFormView:
    model = Book
    template_name = 'form.html'
    success_url = reverse_lazy('list_books')


"""PART 1: List, Create, Update"""
class BookListView(ListView):
    model = Book
    paginate_by = 10
    template_name = 'list.html'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return BookFilter(self.request.GET, queryset=queryset).qs


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

        return response.json().get('items')

    def post(self, request, *args, **kwargs):
        # form data for query filtering in external api
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

        # get the results
        google_api_results = self.get_books_from_external_api(params)

        # create list of books from api where the date format is correct
        if google_api_results:
            book_data = [_parse_book(google_api_results[i]) for i in range(len(google_api_results))]
        else:
            return redirect('list_books')

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
