from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.models import Room
from hotels.serializers import RoomSerializer


class RoomListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint для работы со списком номеров:
    - GET /api/rooms/ -> получить список всех номеров
    - POST /api/rooms/ -> создать новый номер
    """

    queryset = Room.objects.select_related("category").all()
    serializer_class = RoomSerializer


class RoomDestroyAPIView(generics.DestroyAPIView):
    """
    Endpoint для удаления номера:
    - DELETE /api/rooms/<id>/
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class PingAPIView(APIView):
    """
    Простейший health-check endpoint для проверки, что API живой.
    """

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})
