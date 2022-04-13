from django.urls import path

from .views import AddBookFormView, BookListViewSet, ImportBookViewSet, UpdateBookFormView, BookListView

urlpatterns = [
    path('add/', AddBookFormView.as_view(), name="add_book"),
    path('list/', BookListView.as_view(), name="list_books"),
    path('form/update/<int:pk>/', UpdateBookFormView.as_view(), name="update_book"),
    path('all/', BookListViewSet.as_view({"get": "list"}), name="all"),
    path('import/<str:params>/', ImportBookViewSet.as_view({"post": "create"}), name="from_api"),
]
