from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, blank = False, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def user_to_inactive(sender, instance, created, update_fields, **kwargs):
    if created:
        instance.is_active = False
        instance.save()