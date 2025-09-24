from django import forms
from . import models


class AddBookForm(forms.ModelForm):

    class Meta:
        model = models.Book
        fields = (
            'ISBN',
            'title',
            'book_type',
            'serie',
            'number',
            'first_publish_year',
            'description',
        )
