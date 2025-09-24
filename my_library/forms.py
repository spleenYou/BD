from django import forms
from . import models


class AddBookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

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
