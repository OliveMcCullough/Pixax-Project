from django.contrib import admin
from .models import Slideshow, Slide


class SlideInline(admin.TabularInline):
    model = Slide
    extra = 3


class SlideshowAdmin(admin.ModelAdmin):
    model = Slideshow
    inlines = [SlideInline]


admin.site.register(Slideshow, SlideshowAdmin)