from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Quote


class LoadQuote(APIView):

    def get(self, request, format=None):
        quote = Quote.randoms.random()

        response = {
            'id': quote.id,
            'words': quote.content.strip().split(),
        }

        return Response(response, status=status.HTTP_200_OK)
