from django.urls import path

from hotels.views import (
    BookingCreateAPIView,
    BookingDestroyAPIView,
    CategoryListCreateAPIView,
    PingAPIView,
    RoomBookingsListAPIView,
    RoomDestroyAPIView,
    RoomListCreateAPIView,
)

urlpatterns = [
    path("ping/", PingAPIView.as_view(), name="ping"),
    path("rooms/", RoomListCreateAPIView.as_view(), name="room-list-create"),
    path("rooms/<int:pk>/", RoomDestroyAPIView.as_view(), name="room-destroy"),
    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path("bookings/", BookingCreateAPIView.as_view(), name="booking-create"),
    path("bookings/<int:pk>/", BookingDestroyAPIView.as_view(), name="booking-destroy"),
    path(
        "rooms/<int:room_id>/bookings/", RoomBookingsListAPIView.as_view(), name="room-booking-list"
    ),
]
