from __future__ import annotations

from django.contrib.postgres.constraints import ExclusionConstraint
from django.db import models
from django.db.models import F, Q


class RoomCategory(models.Model):
    """Категория номера (например: standard / business / lux)."""

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Уникальный код категории, например 'standard', 'business', 'lux'.",
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Человекочитаемое название категории, например 'Стандарт'.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Категория номера"
        verbose_name_plural = "Категории номеров"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class Room(models.Model):
    """Номер отеля."""

    category = models.ForeignKey(
        RoomCategory,
        on_delete=models.PROTECT,
        related_name="rooms",
    )
    description = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Room(id={self.pk}, category={self.category.code}, price={self.price})"


class Booking(models.Model):
    """Бронирование номера на диапазон дат."""

    room = models.ForeignKey("hotels.Room", on_delete=models.CASCADE, related_name="bookings")

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["date_start"]
        constraints = [
            # 1) Базовая защита: начало строго раньше конца
            models.CheckConstraint(
                condition=Q(date_start__lt=F("date_end")),
                name="booking_start_before_end",
            ),
            # 2) Защита от пересечений в рамках одной комнаты (Postgres)
            ExclusionConstraint(
                name="booking_no_overlap_per_room",
                expressions=[
                    (models.F("room"), "="),
                    (
                        models.Func(
                            models.F("date_start"),
                            models.F("date_end"),
                            models.Value("[)"),
                            function="tstzrange",
                        ),
                        "&&",
                    ),
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"Booking(id={self.pk}, room_id={self.room_id}, {self.date_start}..{self.date_end})"
