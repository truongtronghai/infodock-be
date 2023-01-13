from django.urls import path

from .views import ChartApiView

urlpatterns = [path("", ChartApiView.as_view())]
