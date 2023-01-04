from django.urls import path

from .views import GetUserProfileView

urlpatterns = [
    path("", GetUserProfileView.as_view(), name="get-user-profile"),
]
