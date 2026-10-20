from app.adapters.mock_tools import MockToolsAdapter
from app.domain.models import ReducedTripContext
from app.domain.ports import RebookingCommand


def test_base_scenario_contracts_match_pdf():
    adapter = MockToolsAdapter()
    trip = adapter.get_trip_context("ABC123")
    assert trip["booking_id"] == "ABC123"
    assert len(trip["passengers"]) == 2
    assert trip["_meta"]["completeness"] == "PARTIAL"

    events = adapter.get_operational_events(["S1", "S2"])
    assert "MONITORING_FEED" in events["_meta"]["sources_degraded"]
    assert any(e["event_id"] == "E-1001" for e in events["events"])

    policy = adapter.get_policy_rules("DELAY")
    assert policy["version"] == "POL-DELAY-2026-03"
    assert len(policy["rules"]) == 5

    options = adapter.get_eligible_options(ReducedTripContext.from_trip(trip))
    assert options["_meta"]["ttl_seconds"] == 120
    assert [o["option_id"] for o in options["options"]] == ["O1", "O2", "O3"]


def test_write_tools_and_scenario_switching():
    adapter = MockToolsAdapter()
    cmd = RebookingCommand("O1", "key-abc", "ABC123", ("P1", "P2"))
    status, payload = adapter.create_rebooking_request(cmd)
    assert status == 201
    assert payload["status"] == "PENDING_CONFIRMATION"

    dup_status, _ = adapter.create_rebooking_request(cmd)
    assert dup_status == 409

    hc_status, hc_payload = adapter.create_human_case("POLICY_APPROVAL_REQUIRED", {"booking_id": "ABC123"})
    assert hc_status == 201
    assert hc_payload["queue"] == "DISRUPTION_L2"
