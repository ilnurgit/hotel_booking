from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.models import Booking, Room, RoomCategory
from hotels.serializers import BookingSerializer, RoomCategorySerializer, RoomSerializer
from hotels.services.bookings import create_booking


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    Работа с категориями номеров.

    Эндпоинты:
    - GET  /api/categories/  — список категорий
    - POST /api/categories/  — создание категории
    """

    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer


class RoomListCreateAPIView(generics.ListCreateAPIView):
    """
    Работа со списком номеров.
    Эндпоинты:
    - GET  /api/rooms/ — список номеров (опционально фильтрация по category)
    - POST /api/rooms/ — создание номера
    Дополнительно:
    - поддерживается сортировка через query-параметр ?ordering=
      допустимые поля: price, created_at, category
    """

    serializer_class = RoomSerializer

    filter_backends = [OrderingFilter]
    ordering_fields = ["price", "created_at", "category"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Room.objects.select_related("category").all()

        category_id = self.request.query_params.get("category")
        if category_id:
            if not category_id.isdigit():
                return qs.none()
            qs = qs.filter(category_id=int(category_id))

        return qs


class RoomDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление номера.

    Эндпоинт:
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
    Создание бронирования.

    Эндпоинт:
    - POST /api/bookings/

    Логика вынесена в сервис create_booking():
    - проверка диапазона дат
    - проверка пересечений
    - создание записи Booking
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        room_id = serializer.validated_data["room"].pk
        date_start = serializer.validated_data["date_start"]
        date_end = serializer.validated_data["date_end"]

        booking = create_booking(room_id=room_id, date_start=date_start, date_end=date_end)
        serializer.instance = booking


class BookingDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление бронирования.

    Эндпоинт:
    - DELETE /api/bookings/<pk>/
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class RoomBookingsListAPIView(generics.ListAPIView):
    """
    Список бронирований конкретного номера.

    Эндпоинт:
    - GET /api/rooms/<room_id>/bookings/

    Сортировка: по date_start по возрастанию.
    """

    serializer_class = BookingSerializer

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return (
            Booking.objects.select_related("room", "room__category")
            .filter(room_id=room_id)
            .order_by("date_start")
        )
