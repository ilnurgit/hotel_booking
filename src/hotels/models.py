from __future__ import annotations

from django.db import models


class RoomCategory(models.Model):
    code: models.CharField[str, str] = models.CharField(
        max_length=50,
        unique=True,
        help_text="Уникальный код категории, например 'standard', 'business', 'lux'.",
    )
    name: models.CharField[str, str] = models.CharField(
        max_length=100,
        unique=True,
        help_text="Человекочитаемое название категории, например 'Стандарт'.",
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Категория номера"
        verbose_name_plural = "Категории номеров"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class Room(models.Model):
    category: models.ForeignKey[RoomCategory, RoomCategory] = models.ForeignKey(
        RoomCategory, on_delete=models.PROTECT, related_name="rooms"
    )
    description: models.TextField = models.TextField(max_length=2000)
    price: models.DecimalField = models.DecimalField(max_digits=8, decimal_places=2)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Room(id={self.id}, category={self.category.code}, price={self.price})"
