from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CompanionSettings:
    relevant_delay_min_minutes: int = 1
    clock_skew_seconds: int = 60
    mct_uncertainty_minutes: int = 45
    rebook_max_retries: int = 2
    parser_max_chars: int = 200
    parser_max_depth: int = 10
    remedy_rights: tuple[str, ...] = ("REBOOK_NO_FEE", "MEAL_VOUCHER", "CASH_COMPENSATION")
    change_rights: tuple[str, ...] = ("REBOOK_NO_FEE",)
    supported_event_types: tuple[str, ...] = ("DELAY", "GATE_CHANGE", "STATUS")
    airport_countries: dict[str, str] = field(
        default_factory=lambda: {"SCL": "CL", "LIM": "PE", "MEX": "MX"}
    )
    min_connection_minutes: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class ReducedTripContext:
    booking_id: str
    passengers: list[dict[str, str]]
    has_minor: bool
    segments: list[dict[str, Any]]

    @classmethod
    def from_trip(cls, trip: dict[str, Any]) -> "ReducedTripContext":
        pax = trip.get("passengers", [])
        clean = [_project_passenger(p) for p in pax]
        minor = has_minor_in_group(pax) is not False
        return cls(str(trip.get("booking_id", "")), clean, minor, list(trip.get("segments", [])))


def _project_passenger(passenger: dict[str, Any]) -> dict[str, str]:
    return {
        "passenger_id": str(passenger.get("passenger_id", "")),
        "type": str(passenger.get("type", "UNKNOWN")),
    }


def extract_holder_first_name(passengers: list[dict[str, Any]]) -> str | None:
    for passenger in passengers:
        if passenger.get("type") == "ADULT" and passenger.get("name"):
            return str(passenger["name"]).strip().split()[0]
    return None


def has_minor_in_group(passengers: list[dict[str, Any]]) -> bool | None:
    types = [p.get("type") for p in passengers]
    if "CHILD" in types:
        return True
    if types and all(t == "ADULT" for t in types):
        return False
    return None
