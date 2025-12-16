from datetime import datetime

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from hotels.models import Booking, Room


@transaction.atomic
def create_booking(*, room_id: int, date_start: datetime, date_end: datetime) -> Booking:
    """
    Создать бронирование комнаты.

    Логика:
    - интервал бронирования задаётся как [date_start, date_end)
    - используется select_for_update(), чтобы избежать race-condition
    - защита от пересечений реализована на уровне БД через ExclusionConstraint

    :param room_id: ID комнаты
    :param date_start: дата и время начала бронирования (timezone-aware)
    :param date_end: дата и время окончания бронирования (timezone-aware)
    :return: созданный объект Booking
    :raises ValidationError: если диапазон некорректный или есть пересечение
    """

    # Базовая защита на уровне бизнес-логики
    # (дублируется сериализатором и CheckConstraint, но полезна для явной ошибки)
    if date_start >= date_end:
        raise ValidationError(
            {
                "date_end": (
                    "Дата окончания должна быть позже даты начала "
                    "(используется логика интервала [start, end))."
                )
            }
        )

    # Блокируем строку комнаты до конца транзакции,
    # чтобы два параллельных запроса не создали пересекающиеся брони
    room = get_object_or_404(Room.objects.select_for_update(), pk=room_id)

    try:
        return Booking.objects.create(room=room, date_start=date_start, date_end=date_end)
    except IntegrityError as err:
        # Попадаем сюда, если сработал ExclusionConstraint (пересечение дат)
        raise ValidationError(
            {"non_field_errors": ["Комната уже забронирована на указанный период."]}
        ) from err
