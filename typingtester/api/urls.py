from django.urls import path

from .views import LoadQuote, CsrfRequest

app_name = 'api'
urlpatterns = [
    path('load', LoadQuote.as_view()),
    path('csrf', CsrfRequest.as_view()),
]
