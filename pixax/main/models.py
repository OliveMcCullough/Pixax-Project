from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from django.db.models import Count
from sql_util.utils import SubqueryCount
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from users.models import User


class Slideshow(models.Model):
    """
    Slideshow that can be used on the frontend
    """
    name = models.CharField(max_length=100, unique=True)
    timer = models.PositiveIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(20)])

    def __str__(self):
        return self.name


class Slide(models.Model):
    """
    A slide used in a slideshow
    """
    class FocalPointChoice(models.TextChoices):
        TOP_LEFT = 'top-left', ('Top-left')
        TOP = 'top', ('Top')
        TOP_RIGHT = 'top-right', ('Top-right')
        CENTER_LEFT = 'center-left', ('Center-left')
        CENTER = 'center', ('Center'),
        CENTER_RIGTH = 'center-right', ('Center-right'),
        BOTTOM_LEFT = 'bottom-left', ('Bottom-left'),
        BOTTOM = 'bottom', ('Bottom'),
        BOTTOM_RIGHT = 'bottom-right', ('Bottom-right')

    image = models.ImageField(upload_to='slideshow/')
    slideshow = models.ForeignKey(Slideshow, on_delete=models.CASCADE, related_name='slides')
    focal_point = models.CharField(max_length=20, choices = FocalPointChoice.choices, default='center')


@receiver(pre_delete, sender=Slide)
def delete_uploaded_image(sender, instance, **kwargs):
    slide = instance
    slide.image.delete()


class Album(models.Model):
    """
    An album created by a user that corresponds to a set of photos
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def cover_picture(self):
        return self.ordered_pictures().first()

    def is_empty(self):
        return self.pictures.count() == 0

    def has_unrated(self):
        return self.pictures.filter(rating=None).count() > 0

    def ordered_pictures(self):
        return self.pictures.all().order_by('-rating', '-id')


@receiver(pre_delete, sender=Album)
def delete_exclusive_pictures(sender, instance, **kwargs):
    album = instance
    album.pictures.annotate(num_albums=SubqueryCount('albums')).filter(num_albums=1).delete()


class Picture(models.Model):
    """
    A picture that can be accessed via an album, or via unsorted pictures
    """
    image = models.ImageField(upload_to='pictures/')
    suggested_albums = models.ManyToManyField(Album, related_name='potential_pictures', blank=True, null=True)
    albums = models.ManyToManyField(Album, related_name='pictures', blank=True, null=True)
    rating = models.FloatField(default=None, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pictures')
    date_uploaded = models.DateTimeField(default=datetime.now, blank=True)


@receiver(pre_delete, sender=Picture)
def delete_uploaded_image(sender, instance, **kwargs):
    picture = instance
    picture.image.delete()
