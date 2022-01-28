from django.contrib import admin

from .models import Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('content',)


admin.site.register(Quote, QuoteAdmin)
