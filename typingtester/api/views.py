from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin

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


class StartedTest(APIView, LoginRequiredMixin):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        user = request.user
        user.statistics.tests_started += 1
        user.statistics.save()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class CompletedTest(APIView, LoginRequiredMixin):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        user = request.user
        user.statistics.tests_completed += 1
        user.statistics.save()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class UpdateTotalTestsTime(APIView, LoginRequiredMixin):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        user = request.user
        user.statistics.time_typing += request.data['time']
        user.statistics.save()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)
