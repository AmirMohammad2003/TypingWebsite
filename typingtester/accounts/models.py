from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True,
                              max_length=254, verbose_name='email address')
    is_email_verified = models.BooleanField(default=False)
