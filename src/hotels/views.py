from rest_framework.response import Response
from rest_framework.views import APIView


class PingAPIView(APIView):
    """
    Простейший health-check endpoint для проверки, что API живой.
    """

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})
