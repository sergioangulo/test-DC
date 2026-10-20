from app.adapters.mock_tools import MockToolsAdapter
from app.domain.event_resolver import resolve_events
from app.domain.models import CompanionSettings
from app.domain.variable_deriver import derive_variables


def test_derives_base_case_variables_correctly():
    adapter = MockToolsAdapter("BASE_TC01")
    settings = CompanionSettings()
    trip = adapter.get_trip_context("ABC123")
    events = adapter.get_operational_events(["S1", "S2"])
    res = resolve_events(trip["segments"], events, settings)
    derived = derive_variables(trip, res, settings)

    assert derived.values["delay_minutes"] == 160
    assert derived.values["new_arrival"] == "2026-09-15T20:35"
    assert derived.values["missed_connection"] is True
    assert derived.values["international"] is True
    assert derived.values["group_includes_minor"] is True
    assert derived.values["compensation_requested"] is False
    assert derived.connection_margin_minutes == -90
