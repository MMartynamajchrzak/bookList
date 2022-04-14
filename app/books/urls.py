from django.urls import path

from .views import AddBookFormView, BookListViewSet, UpdateBookFormView, BookListView, ImportBookFormView

urlpatterns = [
    path('add/', AddBookFormView.as_view(), name="add_book"),
    path('list/', BookListView.as_view(), name="list_books"),
    path('import/', ImportBookFormView.as_view(), name="import_books"),
    path('update/<int:pk>/', UpdateBookFormView.as_view(), name="update_book"),
    path('all/', BookListViewSet.as_view({"get": "list"}), name="all"),
]
