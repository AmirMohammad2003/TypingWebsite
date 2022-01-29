"""frontend.apps
Django Application used for the frontend.
"""

from django.apps import AppConfig


class FrontendConfig(AppConfig):
    """Application Configurations for frontend."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frontend'
