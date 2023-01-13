from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class ChartApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "colors": ["#000080", "#00AAEE", "#800080", "#008080"],
            "series": [125, 225, 50, 100],
            "labels": ["Apple", "Mango", "Orange", "Watermelon"],
        }
        return Response(data, status=status.HTTP_200_OK)
