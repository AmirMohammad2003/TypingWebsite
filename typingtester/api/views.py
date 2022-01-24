from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token

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
