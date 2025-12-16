from django.utils.timezone import is_aware
from rest_framework import serializers

from hotels.models import Booking, Room, RoomCategory


class RoomCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории номера.

    Используется:
    - в выдаче списка/деталей категорий
    - вложенно внутри RoomSerializer (read-only)
    """

    class Meta:
        model = RoomCategory
        fields = (
            "id",
            "code",
            "name",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class RoomSerializer(serializers.ModelSerializer):
    """
    Сериализатор номера.

    В выдаче возвращаем полную категорию (category), а при создании/обновлении
    принимаем category_id (write-only), чтобы клиент мог указать категорию по id.
    """

    category = RoomCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=RoomCategory.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Room
        fields = (
            "id",
            "category",
            "category_id",
            "description",
            "price",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class BookingSerializer(serializers.ModelSerializer):
    """
    Сериализатор бронирования.

    Принцип интервалов: [date_start, date_end)
    То есть дата окончания НЕ включается в бронь (это позволяет стыковать брони
    вплотную без пересечения).
    """

    class Meta:
        model = Booking
        fields = (
            "id",
            "room",
            "date_start",
            "date_end",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        date_start = attrs.get("date_start")
        date_end = attrs.get("date_end")

        # Защита от некорректных диапазонов
        if date_start is not None and date_end is not None and date_start >= date_end:
            raise serializers.ValidationError(
                {
                    "date_end": "Дата окончания должна быть позже даты начала "
                    "(логика интервала: [start, end))."
                }
            )

        # При USE_TZ=True желательно работать только с timezone-aware датами
        if date_start is not None and not is_aware(date_start):
            raise serializers.ValidationError(
                {"date_start": "Дата начала должна содержать timezone (например, +03:00 или Z)."}
            )
        if date_end is not None and not is_aware(date_end):
            raise serializers.ValidationError(
                {"date_end": "Дата окончания должна содержать timezone (например, +03:00 или Z)."}
            )

        return attrs
