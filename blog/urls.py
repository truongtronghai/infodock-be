from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet

router = routers.DefaultRouter()
# register router for Category viewset
router.register(r"category", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
