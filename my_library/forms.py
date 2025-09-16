from django import forms
from . import models


class AddBookForm(forms.ModelForm):

    class Meta:
        model = models.Book
        fields = (
            'ISBN',
            'book_type',
            'serie',
            'title',
            'number',
            'authors',
            'publisher',
            'description',
        )
