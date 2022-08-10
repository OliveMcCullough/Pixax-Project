from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 


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
    slideshow = models.ForeignKey(Slideshow, on_delete=models.CASCADE)
    focal_point = models.CharField(max_length=20, choices = FocalPointChoice.choices, default='center')