from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .constants import CORRECT_ISBN_LEN


def validate_isbn(value):
    if not value.isdigit() or len(str(value)) not in CORRECT_ISBN_LEN:
        raise ValidationError(
            _(f"ISBN is a 13 digit International Standard Book Number."
              f" Please input correct number of digits."),
            params={"value": value},
        )
