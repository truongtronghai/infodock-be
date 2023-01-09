from rest_framework import serializers

from .models import FcmRegistrationId


class FcmRegistrationIdSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False)
    registration_id = serializers.CharField(max_length=200, allow_blank=False)
    device_type = serializers.CharField(max_length=10, allow_blank=False)

    class Meta:
        fields = ["email", "registration_id", "device_type"]
