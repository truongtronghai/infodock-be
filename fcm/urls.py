from django.urls import path

from .views import FcmDeviceTokenApiView

urlpatterns = [path("", FcmDeviceTokenApiView.as_view(), name="fcm_device_token")]
