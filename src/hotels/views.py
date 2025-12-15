from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.models import Booking, Room, RoomCategory
from hotels.serializers import BookingSerializer, RoomCategorySerializer, RoomSerializer


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint для категорий:
    - GET /api/categories/ -> список категорий
    - POST /api/categories/ -> создать категорию
    """

    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer


class RoomListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint для работы со списком номеров:
    - GET /api/rooms/ -> получить список всех номеров
    - POST /api/rooms/ -> создать новый номер
    """

    serializer_class = RoomSerializer

    filter_backends = [OrderingFilter]
    ordering_fields = ["price", "created_at", "category"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Room.objects.select_related("category").all()

        category_id = self.request.query_params.get("category")
        if category_id is not None:
            try:
                category_id_int = int(category_id)
            except ValueError:
                return Room.objects.none()
            qs = qs.filter(category_id=category_id_int)

        return qs


class RoomDestroyAPIView(generics.DestroyAPIView):
    """
    Endpoint для удаления номера:
    - DELETE /api/rooms/<pk>/
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class PingAPIView(APIView):
    """
    Простейший health-check endpoint для проверки, что API живой.
    """

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})


class BookingCreateAPIView(generics.CreateAPIView):
    """
    POST /api/bookings/
    Создать бронь (пока без проверки пересечений).
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingDestroyAPIView(generics.DestroyAPIView):
    """
    DELETE /api/bookings/<pk>
    Удалить бронь.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class RoomBookingsListAPIView(generics.ListAPIView):
    """
    GET /api/rooms/<room_id>/bookings/
    Список броней конкретной комнаты, сортировка по date_start.
    """

    serializer_class = BookingSerializer

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return Booking.objects.filter(room_id=room_id).order_by("date_start")
