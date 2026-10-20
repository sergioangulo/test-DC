from dataclasses import dataclass, field
from typing import Any, Protocol
from app.domain.models import ReducedTripContext


@dataclass(frozen=True)
class RebookingCommand:
    option_id: str
    idempotency_key: str
    booking_id: str
    passenger_ids: tuple[str, ...]


class ToolsPort(Protocol):
    def get_trip_context(self, booking_id: str) -> dict[str, Any]: ...
    def get_operational_events(self, segment_ids: list[str]) -> dict[str, Any]: ...
    def get_policy_rules(self, scenario: str) -> dict[str, Any]: ...
    def get_eligible_options(self, context: ReducedTripContext) -> dict[str, Any]: ...
    def create_rebooking_request(self, command: RebookingCommand) -> tuple[int, dict[str, Any]]: ...
    def create_human_case(self, reason: str, evidence: dict[str, Any]) -> tuple[int, dict[str, Any]]: ...


class ClockPort(Protocol):
    def now_iso(self) -> str: ...


@dataclass
class FixedClock:
    current_iso: str = "2026-09-15T11:02:35Z"

    def now_iso(self) -> str:
        return self.current_iso


@dataclass
class InMemoryDecisionStore:
    decisions: dict[str, dict[str, Any]] = field(default_factory=dict)
    operations: dict[str, dict[str, Any]] = field(default_factory=dict)
    human_cases: dict[str, dict[str, Any]] = field(default_factory=dict)

    def save_decision(self, record: dict[str, Any]) -> None:
        self.decisions[str(record["decision_id"])] = record

    def get_decision(self, decision_id: str) -> dict[str, Any] | None:
        return self.decisions.get(decision_id)
