import pytest
from rest_framework.test import APIClient

from hotels.models import Room, RoomCategory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def category() -> RoomCategory:
    return RoomCategory.objects.create(code="standard", name="Стандарт")


@pytest.fixture
def room(category: RoomCategory) -> Room:
    return Room.objects.create(category=category, description="Test room", price="100.00")


def test_create_booking_ok(api_client: APIClient, room: Room):
    resp = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": "2025-06-20", "date_end": "2025-06-25"},
        format="json",
    )
    assert resp.status_code == 201
    assert resp.data["room"] == room.id


def test_create_booking_reject_invalid_range(api_client: APIClient, room: Room):
    resp = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": "2025-06-25", "date_end": "2025-06-20"},
        format="json",
    )
    assert resp.status_code == 400
    assert "date_end" in resp.data


def test_create_booking_reject_overlap(api_client: APIClient, room: Room):
    # первая бронь
    resp1 = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": "2025-06-20", "date_end": "2025-06-25"},
        format="json",
    )
    assert resp1.status_code == 201

    # пересекающаяся бронь должна быть запрещена
    resp2 = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": "2025-06-23", "date_end": "2025-06-27"},
        format="json",
    )
    assert resp2.status_code == 400
    assert "non_field_errors" in resp2.data


def test_create_booking_allow_touching_ranges(api_client: APIClient, room: Room):
    resp1 = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": "2025-06-20", "date_end": "2025-06-25"},
        format="json",
    )
    assert resp1.status_code == 201

    # start == previous end -> разрешено в [start, end)
    resp2 = api_client.post(
        "/api/bookings/",
        {"room": room.id, "date_start": "2025-06-25", "date_end": "2025-06-27"},
        format="json",
    )
    assert resp2.status_code == 201
