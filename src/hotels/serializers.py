from rest_framework import serializers

from hotels.models import Booking, Room, RoomCategory


class RoomCategorySerializer(serializers.ModelSerializer):
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

        if date_start is not None and date_end is not None and date_start >= date_end:
            raise serializers.ValidationError(
                {"date_end": "date_end must be after date_start (we use [start, end) logic)."}
            )

        return attrs
