from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserProfileSerializer


# Create your views here.
class GetUserProfileView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        # when login successfully, request.user contains object of current user
        date_of_birth = date_of_birth = datetime(
            year=request.data["date_of_birth"]["year"],
            month=request.data["date_of_birth"]["month"],
            day=request.data["date_of_birth"]["day"],
        ).date()
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user, date_of_birth=date_of_birth
        )

        return Response(
            {
                "message": "This is your profile",
                "data": UserProfileSerializer(profile).data,
            },
            status.HTTP_200_OK,
        )


class UpdateAvatarView:
    pass
