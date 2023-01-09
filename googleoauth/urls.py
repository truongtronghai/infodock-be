from django.urls import path

from .views import GoogleAuthApiView

urlpatterns = [
    path("v1/auth/login/google/", GoogleAuthApiView.as_view(), name="google_auth"),
]
