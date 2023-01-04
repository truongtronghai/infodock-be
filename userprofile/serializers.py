from dataclasses import field

from pyexpat import model
from rest_framework.serializers import ModelSerializer, Serializer

from .models import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
