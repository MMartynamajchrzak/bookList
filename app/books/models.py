from django.core.validators import URLValidator
from django.db import models

import books.constants as constants
from .validators import validate_isbn


class Book(models.Model):
    title = models.CharField(max_length=constants.SHORT_TEXT_LENGTH)
    author = models.CharField(max_length=constants.SHORT_TEXT_LENGTH)
    published_date = models.DateField()
    ISBN = models.CharField(max_length=constants.ISBN_MAX_LENGTH, validators=[validate_isbn])
    pages_count = models.IntegerField(blank=True, null=True)
    cover_link = models.URLField(validators=[URLValidator], max_length=constants.LONG_TEXT_LENGTH, blank=True)
    language = models.CharField(max_length=constants.SHORT_TEXT_LENGTH)

    def __str__(self):
        return f"{self.title}, {self.author}"
