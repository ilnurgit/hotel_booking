import pytest
from rest_framework.test import APIClient

from hotels.models import Room, RoomCategory

pytestmark = pytest.mark.django_db

# Используем timezone-aware datetime в ISO-формате,
# чтобы тесты не зависели от TZ/настроек окружения.
START_1 = "2025-06-20T00:00:00+03:00"
END_1 = "2025-06-25T00:00:00+03:00"

START_OVERLAP = "2025-06-23T00:00:00+03:00"
END_OVERLAP = "2025-06-27T00:00:00+03:00"

START_TOUCH = END_1
END_TOUCH = "2025-06-27T00:00:00+03:00"


@pytest.fixture
def api_client() -> APIClient:
    """DRF клиент для запросов к API."""
    return APIClient()


@pytest.fixture
def category() -> RoomCategory:
    """Категория номера для тестов."""
    return RoomCategory.objects.create(code="standard", name="Стандарт")


@pytest.fixture
def room(category: RoomCategory) -> Room:
    """Комната для тестов бронирований."""
    return Room.objects.create(category=category, description="Test room", price="100.00")


def test_create_booking_ok(api_client: APIClient, room: Room) -> None:
    """Успешное создание бронирования."""
    resp = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": START_1, "date_end": END_1},
        format="json",
    )
    assert resp.status_code == 201
    assert resp.data["room"] == room.id


def test_create_booking_reject_invalid_range(api_client: APIClient, room: Room) -> None:
    """Нельзя создать бронь, если date_start >= date_end."""
    resp = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": END_1, "date_end": START_1},
        format="json",
    )
    assert resp.status_code == 400
    assert "date_end" in resp.data


def test_create_booking_reject_overlap(api_client: APIClient, room: Room) -> None:
    """Пересекающееся бронирование должно быть запрещено."""
    resp1 = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": START_1, "date_end": END_1},
        format="json",
    )
    assert resp1.status_code == 201

    resp2 = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": START_OVERLAP, "date_end": END_OVERLAP},
        format="json",
    )
    assert resp2.status_code == 400
    assert "non_field_errors" in resp2.data


def test_create_booking_allow_touching_ranges(api_client: APIClient, room: Room) -> None:
    """
    Бронирования вида:
    [2025-06-20, 2025-06-25) и [2025-06-25, 2025-06-27)
    НЕ пересекаются, поэтому второе должно быть разрешено.
    """
    resp1 = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": START_1, "date_end": END_1},
        format="json",
    )
    assert resp1.status_code == 201

    resp2 = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": START_TOUCH, "date_end": END_TOUCH},
        format="json",
    )
    assert resp2.status_code == 201
