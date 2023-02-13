from django.urls import path
from .views import UploadImageApiView

urlpatterns = [
    path("", UploadImageApiView.as_view(), name="upload_image"),
]
