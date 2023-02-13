from django.urls import include, path
from rest_framework import routers

# from .views import (CategoryViewSet, DetailPostApiView, ListPostApiView,
#                     SearchPostApiView)
from .views.categoryViewset import CategoryViewSet
from .views.detailPostApiview import DetailPostApiView
from .views.listPostApiview import ListPostApiView
from .views.searchPostApiview import SearchPostApiView

router = routers.DefaultRouter()
# register router for Category viewset
router.register("category", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("posts/<slug:slug>/", ListPostApiView.as_view(), name="list_post"),
    path("<slug:slug>/", DetailPostApiView.as_view(), name="detail_post"),
    path(
        "search/<str:search_string>/", SearchPostApiView.as_view(), name="search_post"
    ),
]
