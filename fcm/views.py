from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FcmRegistrationId
from .serializers import FcmRegistrationIdSerializer


# Create your views here.
class FcmDeviceTokenApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FcmRegistrationIdSerializer(data=request.data)
        if serializer.is_valid():
            try:
                FcmRegistrationId.objects.get_or_create(
                    registrationId=serializer.validated_data["registration_id"],
                    deviceType=serializer.validated_data["device_type"],
                    user=User.objects.get(email=serializer.validated_data["email"]),
                )
                return Response(
                    {"detail": "Registration ID has been created successfully"},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {"detail": "User with the email does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except MultipleObjectsReturned:
                return Response(
                    {"detail": "Got multiple registration ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except IntegrityError:
                return Response(
                    {"detail": "Registration ID exists. Cannot save duplicate ids"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
