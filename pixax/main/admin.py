from django import forms
from django.contrib import admin
from django.contrib.admin.decorators import display
from django.utils.html import format_html
import uuid

from .models import Slideshow, Slide, Picture, Album
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
    list_display = ('user', 'get_albums', 'image', 'date_uploaded')
    search_fields = ['user__username', 'albums__name', 'image']

    @display(description='Albums')
    def get_albums(self, obj):
        return "\n".join([album.name for album in obj.albums.all()])


class SharedToUsersInline(admin.TabularInline):
    model = Album.shared_with.through
    extra = 0
    readonly_fields = ["user_username"]
    verbose_name = "Shared with"
    verbose_name_plural = "Shared with"

    def user_username(self, instance):
        return instance.user.username

    def has_add_permission(self, request, obj=None): 
        return False
    
    def has_change_permission(self, request, obj=None): 
        return False

    def has_delete_permission(self, request, obj=None): 
        return False


class PictureInline(admin.TabularInline):
    model = Album.pictures.through
    extra = 0
    readonly_fields = ['picture_image']
    verbose_name = "Album"
    verbose_name_plural = "Albums"

    def picture_image(self, instance):
        return format_html("<a href=" + instance.picture.image.url + ">" + str(instance.picture.image) + "</a>")

    def has_add_permission(self, request, obj=None): 
        return False
    
    def has_change_permission(self, request, obj=None): 
        return False

    def has_delete_permission(self, request, obj=None): 
        return False


class AlbumAdmin(admin.ModelAdmin):
    model = Album
    fields = ('name', 'share_status', 'author')
    readonly_fields = ('author',)
    list_display = ('name', 'author', 'get_pictures')
    inlines = [PictureInline, SharedToUsersInline]

    @display(description='Pictures')
    def get_pictures(self, obj):
        pictures = obj.pictures
        return pictures.count()


admin.site.register(Album, AlbumAdmin)
admin.site.register(Slideshow, SlideshowAdmin)
admin.site.register(Picture, PictureAdmin)