from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True,
                              max_length=254, verbose_name='email address')
    is_email_verified = models.BooleanField(default=False)

    def set_email_verified(self, value):
        self.is_email_verified = value
        self.save()
