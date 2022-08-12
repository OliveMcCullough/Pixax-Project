from django import forms
from django.core.exceptions import ValidationError

from .models import Album


class AlbumCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Album
        fields = ['name']