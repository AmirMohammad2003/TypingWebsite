"""accounts.app
Django Application used for authentication and authorization.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Application Configurations for accounts.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
