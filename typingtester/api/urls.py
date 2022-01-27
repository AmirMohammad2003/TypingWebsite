from django.urls import path

from .views import LoadQuote, CsrfRequest, StartedTest, CompletedTest, UpdateTotalTestsTime

app_name = 'api'
urlpatterns = [
    path('load/', LoadQuote.as_view()),
    path('csrf/', CsrfRequest.as_view()),
    path('started-test/', StartedTest.as_view()),
    path('completed-test/', CompletedTest.as_view()),
    path('update-total-tests-time/', UpdateTotalTestsTime.as_view()),
]
