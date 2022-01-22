from django.urls import path

from .views import LoadQuote

app_name = 'api'
urlpatterns = [
    path('load', LoadQuote.as_view()),
]
