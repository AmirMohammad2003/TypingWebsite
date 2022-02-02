"""api.views
Views used for the API.
"""

from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quote
from .serializers import RecordSerializer


class LoadQuote(APIView):
    """
    LoadQuote
    Loads a random quote from the database.
    """

    @method_decorator(csrf_exempt)
    def get(self, request):  # pylint: disable=unused-argument, no-self-use
        """
        get a random quote.
        """
        quote = Quote.randoms.random()

        response = {
            'id': quote.id,
            'words': quote.content.strip().split(),
        }

        return Response(response, status=status.HTTP_200_OK)


class CsrfRequest(APIView):
    """
    CsrfRequest
    Returns a CSRF token.
    """

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):  # pylint: disable=no-self-use
        """
        get the CSRF token.
        :param request:
        :return: the CSRF token.
        """

        return Response({'token': get_token(request)}, status=status.HTTP_200_OK)


class StartedTest(APIView):
    """
    StartedTest
    tells the server the user has started a new test.
    only authenticated users can use this view.
    accepts post requests.
    """

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):  # pylint: disable=no-self-use
        """
        :param request:
        increments the number of tests started by the user.
        """
        user = request.user
        user.statistics.tests_started += 1
        user.statistics.save()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class CompletedTest(APIView):
    """
    CompletedTest
    tells the server the user has completed a test.
    only authenticated users can use this view.
    accepts post requests.
    """

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):  # pylint: disable=no-self-use
        """
        :param request:
        :param format:
        increments the number of tests completed by the user.
        """
        user = request.user
        user.statistics.tests_completed += 1
        user.statistics.save()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class UpdateTotalTestsTime(APIView):
    """
    UpdateTotalTestsTime
    tells the server the user has completed a test.
    only authenticated users can use this view.
    accepts post requests.
    """

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):   # pylint: disable=no-self-use
        """
        :param request:
        receives the time the user spent on the test.
        increments the total time spent on tests by the user.
        """
        time = float(request.data['time'])
        if time < 0:
            return Response(
                {
                    'success': 'false',
                    'error': 'time cannot be negative'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user.statistics.time_typing += time
        user.statistics.save()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class InsertUserTest(APIView):
    """
    InsertUserTest
    inserts a new test record for the user.
    only authenticated users can use this view.
    accepts post requests.
    """

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):  # pylint: disable=no-self-use
        """
        :param request:
        receives the time, cpm, acc and quote_id from the request.
        """
        time = float(request.data['time'])
        cpm = float(request.data['cpm'])
        acc = float(request.data['acc'])
        quote_id = int(request.data['quote_id'])
        if time < 0 or cpm < 0 or acc < 0 or quote_id < 0:
            return Response(
                {'success': 'false', 'error': 'invalid input'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user.tests.create(
            time=time,
            cpm=cpm,
            accuracy=acc,
            quote_id=quote_id
        )

        return Response({'success': 'true'}, status=status.HTTP_201_CREATED)


class LoadTestRecords(ListAPIView):
    """
    LoadTestRecords
    loads all test records for the user.
    only authenticated users can use this view.
    accepts get requests.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RecordSerializer

    def get_queryset(self):
        """
        :return: all test records for the user.
        """
        return self.request.user.tests.all()


class LoadStatistics(APIView):
    """
    LoadStatistics
    loads all statistics for the user.
    only authenticated users can use this view.
    accepts post requests.
    """

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):  # pylint: disable=no-self-use
        """
        :param request:
        :return all statistics for the user.
        """
        user = request.user
        statistics = user.statistics
        response = {
            'tests_started': statistics.tests_started,
            'tests_completed': statistics.tests_completed,
            'time_typing': statistics.time_typing
        }
        return Response(response, status=status.HTTP_200_OK)
