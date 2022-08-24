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
    same_or_different_albums=forms.ChoiceField(label='Are these pictures', choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        album_list = Album.objects.filter(author=user).order_by(Lower('name'))
        self.fields['which_albums'] = forms.MultipleChoiceField(
            choices=[(album.id, str(album)) for album in album_list],
            widget=CustomCheckboxSelectMultiple
        )


class RateAndSortIntroForm(forms.Form):
    ORDER_CHOICES = [
        ("-rating","Highest rating"),
        ("rating","Lowest rating"),
        ("-date_uploaded","Newest"),
        ("date_uploaded","Oldest")
    ]
    RATE_SORT_CHOICES = [
        ("both","Rate and Sort"),
        ("rate_only","Rate"),
        ("sort_only", "Sort")
    ]
    
    order_select = forms.ChoiceField(label="Navigate pictures in which order?", choices=ORDER_CHOICES)
    rate_sort_select = forms.ChoiceField(label="Rate or sort the pictures?", choices=RATE_SORT_CHOICES)
    only_rate_unrated_pics = forms.BooleanField(label="Limit rating to unrated pictures?", required = False)


    def __init__(self, default_ordering, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_select'].initial=default_ordering


class RateAndSortActiveForm(forms.Form):
    rating = forms.FloatField(label="Rating", required=False)
    id = forms.IntegerField(widget = forms.HiddenInput)
    albums = forms.MultipleChoiceField(
        widget=CustomCheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Picture
        fields = ["albums","rating", "id"]
        exclude = ["user_id"]

    def __init__(self, instance, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        album_list = Album.objects.filter(author=user).order_by(Lower('name'))
        self.fields['albums'].choices= [(album.id, str(album)) for album in album_list]
        self.initial['albums'] = [album.id for album in instance.albums.all()] 
        self.initial['rating'] = instance.rating
        self.initial['id'] = instance.id
        