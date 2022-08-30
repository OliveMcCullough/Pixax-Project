from django import forms
from django.forms import inlineformset_factory
from django.contrib import admin
import uuid

from .models import Slideshow, Slide, Picture
from .services import remove_exif


class SlideInlineForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ["image", "focal_point"]

    def clean_image(self):
        image = self.cleaned_data['image']
        if not "slideshow/" in image:
            unique_base_file_name = str(uuid.uuid4())
            image = remove_exif(image, unique_base_file_name, "pictures/")
            return image


class SlideInline(admin.TabularInline):
    model = Slide
    extra = 3
    form = SlideInlineForm


class SlideshowAdmin(admin.ModelAdmin):
    model = Slideshow
    fields = ['name', 'timer']
    inlines = [
        SlideInline
    ]


class PictureAdmin(admin.ModelAdmin):
    model = Picture
    readonly_fields = ('image','user', 'date_uploaded', 'albums', 'suggested_albums', 'rating')


admin.site.register(Slideshow, SlideshowAdmin)
admin.site.register(Picture, PictureAdmin)