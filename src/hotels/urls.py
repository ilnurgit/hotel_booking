from django.urls import path

from .views import PingAPIView

urlpatterns = [
    path("ping/", PingAPIView.as_view(), name="ping"),
]
