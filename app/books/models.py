from django.core.validators import URLValidator
from django.db import models

import books.constants as constants
from .validators import validate_isbn


class Book(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=constants.MAGIC_NUMBER)
    author = models.CharField(max_length=constants.SHORT_TEXT_LENGTH)
    published_date = models.DateField(blank=True, null=True)
    ISBN = models.CharField(max_length=constants.ISBN_MAX_LENGTH, validators=[validate_isbn], blank=True, null=True)
    pages_count = models.IntegerField(blank=True, null=True)
    cover_link = models.URLField(validators=[URLValidator], max_length=constants.LONG_TEXT_LENGTH, blank=True, null=True)
    language = models.CharField(max_length=constants.SHORT_TEXT_LENGTH)

    def __str__(self) -> str:
        return f"{self.title}, {self.author}"
