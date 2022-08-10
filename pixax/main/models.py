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
    CHOICES = (
        ('top-left', 'Top-left'),
        ('top','Top'),
        ('top-right','Top-Right'),
        ('center-left', 'Center'),
        ('center', 'Center'),
        ('center-right', 'Center-Right'),
        ('bottom-left', 'Bottom-Left'),
        ('bottom', 'Bottom'),
        ('bottom-right', 'Bottom-Right')
    )
    image = models.ImageField(upload_to='slideshow/')
    slideshow = models.ForeignKey(Slideshow, on_delete=models.CASCADE)
    focal_point = models.CharField(max_length=20, choices = CHOICES, default='center')