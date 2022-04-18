from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'ISBN', 'pages_count', 'cover_link', 'language']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            'title',
            'author',
            'published_date',
            'ISBN',
            'pages_count',
            'cover_link',
            'language',
            Submit('submit', 'Submit', css_class='btn-success')
        )


class GoogleSearchForm(forms.ModelForm):
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)

    class Meta:
        model = Book
        fields = ['title', 'author', 'ISBN']
