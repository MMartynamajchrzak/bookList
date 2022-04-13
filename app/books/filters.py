import django_filters
from django_filters import rest_framework as filters

from .models import Book


class BaseFilter:
    class Meta:
        model = Book

        fields = {
            'title': ['icontains'],
            'author': ['icontains'],
            'language': ['exact']
        }


class BookFilter(BaseFilter, django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='published_date', lookup_expr='lte')


class BookRestFilter(BaseFilter, filters.FilterSet):
    from_date = filters.DateFilter(field_name='published_date', lookup_expr='gte')
    to_date = filters.DateFilter(field_name='published_date', lookup_expr='lte')
