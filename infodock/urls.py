from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi  # need for DRF-YASG
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="InfoDock",
        default_version="v1",
        description="A blog API",
        terms_of_service="",
        contact=openapi.Contact(email="hai.truong@datafluct.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),  # auto urls from DRF
    path("admin/", admin.site.urls),
    path("user-profile/", include("userprofile.urls")),
    path("blog/", include("blog.urls")),
    path("user/device-token/", include("fcm.urls")),
    path("googleoauth/", include("googleoauth.urls")),
    path("chart/", include("chart.urls")),
    path("rest-auth/", include("rest_framework.urls")),
    # SimpleJWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # urls of drf-yasg
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    # CKEditor
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
]
# used for serving
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
