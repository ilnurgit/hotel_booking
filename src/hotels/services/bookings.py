from datetime import date

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from hotels.models import Booking, Room


@transaction.atomic
def create_booking(*, room_id: int, date_start: date, date_end: date) -> Booking:
    if date_start >= date_end:
        raise ValidationError(
            {"date_end": "date_end must be after date_start (we use [start, end) logic)."}
        )

    room = get_object_or_404(Room.objects.select_for_update(), pk=room_id)

    try:
        return Booking.objects.create(room=room, date_start=date_start, date_end=date_end)
    except IntegrityError as err:
        # сюда попадём, если exclusion constraint запретил пересечение
        raise ValidationError(
            {"non_field_errors": ["Room is already booked for these dates."]}
        ) from err
