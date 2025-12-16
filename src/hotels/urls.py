"""
URL-конфигурация приложения hotels.

Назначение:
- health-check эндпоинт
- управление категориями номеров
- управление номерами
- управление бронированиями
- просмотр бронирований конкретного номера

Все эндпоинты возвращают и принимают данные в формате JSON (REST API).
"""

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
    # Health-check / технический эндпоинт
    path("ping/", PingAPIView.as_view(), name="ping"),
    # Номера
    path("rooms/", RoomListCreateAPIView.as_view(), name="room-list-create"),
    path("rooms/<int:pk>/", RoomDestroyAPIView.as_view(), name="room-destroy"),
    # Категории номеров
    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list-create"),
    # Бронирования
    path("bookings/", BookingCreateAPIView.as_view(), name="booking-create"),
    path("bookings/<int:pk>/", BookingDestroyAPIView.as_view(), name="booking-destroy"),
    # Список бронирований конкретного номера
    path(
        "rooms/<int:room_id>/bookings/",
        RoomBookingsListAPIView.as_view(),
        name="room-booking-list",
    ),
]
