from __future__ import annotations

from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateRangeField
from django.contrib.postgres.fields.ranges import RangeOperators
from django.db import models
from django.db.models import F, Func, Q, Value


class RoomCategory(models.Model):
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
        # id всегда есть на сохранённом объекте; для удобства читаемости ок
        return f"Room(id={self.pk}, category={self.category.code}, price={self.price})"


class Booking(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    # Важно: используем [start, end) логику на уровне БД через daterange(..., '[)')
    date_start = models.DateField()
    date_end = models.DateField()

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
                    (F("room"), RangeOperators.EQUAL),
                    (
                        Func(
                            F("date_start"),
                            F("date_end"),
                            Value("[)"),
                            function="daterange",
                            output_field=DateRangeField(),
                        ),
                        RangeOperators.OVERLAPS,
                    ),
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"Booking(id={self.pk}, room_id={self.room_id}, {self.date_start}..{self.date_end})"
