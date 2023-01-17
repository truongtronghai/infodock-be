from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import time

# Create your views here.
class ChartApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "colors": ["#FF8B13", "#F273E6", "#FFEA20", "#B05A7A"],
            "series": [125, 225, 50, 100],
            "labels": ["Apple", "Mango", "Orange", "Watermelon"],
        }
        time.sleep(5)
        return Response(data, status=status.HTTP_200_OK)
