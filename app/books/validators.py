from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .constants import VALID_ISBN_LEN


def validate_isbn(value):
    if not value.isdigit() or len(str(value)) not in VALID_ISBN_LEN:
        raise ValidationError(
            _("ISBN is a 13 digit International Standard Book Number."
              " Please input correct number of digits."),
            params={"value": value},
        )


def validate_date(value):
    date_formats = ["%Y-%m-%d", "%Y-%m", "%Y"]

    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(value, date_format)
        except ValueError:
            continue
        else:
            return parsed_date.date()
