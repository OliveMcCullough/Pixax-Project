from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, blank = False, null=False)
    application_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.username