from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated

from .models import Quote


class LoadQuote(APIView):

    @method_decorator(csrf_exempt)
    def get(self, request, format=None):
        quote = Quote.randoms.random()

        response = {
            'id': quote.id,
            'words': quote.content.strip().split(),
        }

        return Response(response, status=status.HTTP_200_OK)


class CsrfRequest(APIView):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None):
        return Response({'token': get_token(request)}, status=status.HTTP_200_OK)


class StartedTest(APIView):

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        user = request.user
        user.statistics.tests_started += 1
        user.statistics.save()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class CompletedTest(APIView):

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        user = request.user
        user.statistics.tests_completed += 1
        user.statistics.save()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class UpdateTotalTestsTime(APIView):

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        user = request.user
        user.statistics.time_typing += float(request.data['time'])
        user.statistics.save()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class InsertUserTest(APIView):

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        user = request.user
        user.tests.create(
            time=float(request.data['time']),
            cpm=int(request.data['cpm']),
            accuracy=int(request.data['acc']),
            quote_id=int(request.data['quote_id'])
        )

        return Response({'success': 'true'}, status=status.HTTP_201_CREATED)


class LoadTestRecords(APIView):

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        user = request.user
        tests = user.tests.all()
        response = []
        for test in tests:
            response.append({
                'time': test.time,
                'cpm': test.cpm,
                'acc': test.accuracy,
                'quote_id': test.quote_id
            })
        return Response(response, status=status.HTTP_200_OK)


class LoadStatistics(APIView):

    permission_classes = (IsAuthenticated,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        user = request.user
        statistics = user.statistics
        response = {
            'tests_started': statistics.tests_started,
            'tests_completed': statistics.tests_completed,
            'time_typing': statistics.time_typing
        }
        return Response(response, status=status.HTTP_200_OK)
