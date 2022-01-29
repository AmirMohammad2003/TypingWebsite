"""api.admin
model registration for api application.
"""

from django.contrib import admin

from .models import Quote


class QuoteAdmin(admin.ModelAdmin):
    """
    Custom QuoteAdmin
    """
    search_fields = ('content',)
    ordering = ('-created',)
    list_display = ('content',)


admin.site.register(Quote, QuoteAdmin)
