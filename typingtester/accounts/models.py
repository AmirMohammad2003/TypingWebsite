"""accounts.models
Django models for accounts app.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model.
    Inherited from the built-in User model.
    makes the email field to be required and unique.
    and adds a is_email_verified field.
    """
    email = models.EmailField(blank=False, unique=True,
                              max_length=254, verbose_name='email address')
    is_email_verified = models.BooleanField(default=False)
