from django.contrib import admin
from .models import Slideshow, Slide, Picture


class SlideInline(admin.TabularInline):
    model = Slide
    extra = 3


class SlideshowAdmin(admin.ModelAdmin):
    model = Slideshow
    inlines = [SlideInline]


class PictureAdmin(admin.ModelAdmin):
    model = Picture


admin.site.register(Slideshow, SlideshowAdmin)
admin.site.register(Picture, PictureAdmin)