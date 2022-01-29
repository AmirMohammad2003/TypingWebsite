"""api.apps
Django Application used for the API.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Application Configurations for api."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from . import signals  # pylint: disable=unused-import, import-outside-toplevel
