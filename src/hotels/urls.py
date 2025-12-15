from django.urls import path

from hotels.views import (
    PingAPIView,
    RoomDestroyAPIView,
    RoomListCreateAPIView,
)

urlpatterns = [
    path("ping/", PingAPIView.as_view(), name="ping"),
    path("rooms/", RoomListCreateAPIView.as_view(), name="room-list-create"),
    path("rooms/<int:pk>", RoomDestroyAPIView.as_view(), name="room-destroy"),
]
