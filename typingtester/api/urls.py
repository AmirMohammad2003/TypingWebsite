"""api.urls
url routings for the api application.
"""

from django.urls import path

from .views import (CompletedTest, CsrfRequest, InsertUserTest, LoadQuote,
                    LoadStatistics, LoadTestRecords, StartedTest,
                    UpdateTotalTestsTime)

app_name = 'api'  # pylint: disable=invalid-name
urlpatterns = [
    path('load/', LoadQuote.as_view(), name='load'),
    path('csrf/', CsrfRequest.as_view(), name='csrf'),
    path('started-test/', StartedTest.as_view(), name='started-test'),
    path('completed-test/', CompletedTest.as_view(), name='completed-test'),
    path('update-total-tests-time/', UpdateTotalTestsTime.as_view(),
         name='update-total-tests-time'),
    path('insert-user-test/', InsertUserTest.as_view(), name='insert-user-test'),
    path('load-statistics/', LoadStatistics.as_view(), name='load-statistics'),
    path('load-test-records/', LoadTestRecords.as_view(), name='load-test-records'),
]
