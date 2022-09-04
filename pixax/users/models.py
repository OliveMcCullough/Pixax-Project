from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)


class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField('email address', unique=True, blank = False, null=False)
    is_active = models.BooleanField(default=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True, default=None)
    username = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def user_to_inactive(sender, instance, created, update_fields, **kwargs):
    if created:
        instance.is_active = False
        instance.save()