from app.domain.models import (
    CompanionSettings,
    ReducedTripContext,
    extract_holder_first_name,
    has_minor_in_group,
)


def test_extract_holder_first_name_and_minor_detection():
    passengers = [
        {"passenger_id": "P1", "name": "Ana Prueba", "type": "ADULT"},
        {"passenger_id": "P2", "name": "Lucas Prueba", "type": "CHILD", "age": 8},
    ]
    assert extract_holder_first_name(passengers) == "Ana"
    assert has_minor_in_group(passengers) is True


def test_reduced_context_strips_personal_data():
    trip = {
        "booking_id": "ABC123",
        "passengers": [
            {"passenger_id": "P1", "name": "Ana Prueba", "type": "ADULT", "document": "123"},
            {"passenger_id": "P2", "name": "Lucas Prueba", "type": "CHILD", "age": 8},
        ],
        "segments": [{"segment_id": "S1", "origin": "SCL", "destination": "LIM"}],
    }
    reduced = ReducedTripContext.from_trip(trip)
    assert reduced.booking_id == "ABC123"
    assert reduced.has_minor is True
    assert reduced.passengers == [
        {"passenger_id": "P1", "type": "ADULT"},
        {"passenger_id": "P2", "type": "CHILD"},
    ]
    assert isinstance(CompanionSettings(), CompanionSettings)
