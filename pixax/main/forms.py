from django import forms
from django.db.models.functions import Lower

from .models import Album, Picture
from .services import CustomCheckboxSelectMultiple


class AlbumCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Album
        fields = ['name']


class PictureUploadForm(forms.Form):
    CHOICES =[("same","all part of the same album(s)?"),("different","part of different albums?")]

    picture_files = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label="")
    same_or_different_albums=forms.CharField(label='Are these pictures', widget=forms.RadioSelect(choices=CHOICES))

    def __init__(self, user, *args, **kwargs):
        super(PictureUploadForm, self).__init__(*args, **kwargs)
        album_list = Album.objects.filter(author=user).order_by(Lower('name'))
        self.fields['which_albums'] = forms.MultipleChoiceField(
            choices=[(album.id, str(album)) for album in album_list],
            widget=CustomCheckboxSelectMultiple
        )