from app.adapters.mock_tools import BASE_OPTIONS, BASE_POLICY, BASE_SEGMENTS
from app.domain.models import CompanionSettings
from app.domain.option_filter import OptionFilterContext, filter_options
from app.domain.rule_engine import evaluate_policy


def test_filters_base_case_options_and_selects_o1():
    settings = CompanionSettings()
    variables = {
        "delay_minutes": 160,
        "international": True,
        "missed_connection": True,
        "compensation_requested": False,
        "group_includes_minor": True,
        "new_arrival": "2026-09-15T20:35",
    }
    pol = evaluate_policy(BASE_POLICY, variables, settings)
    payload = {"options": BASE_OPTIONS, "_meta": {"retrieved_at": "2026-09-15T11:02:35Z", "ttl_seconds": 120}}
    ctx = OptionFilterContext(
        passenger_count=2,
        segments=BASE_SEGMENTS,
        affected_segment_id="S1",
        variables=variables,
        policy=pol,
        now_iso="2026-09-15T11:02:47Z",
    )
    res = filter_options(payload, ctx, settings)

    assert [o["option_id"] for o in res.viable] == ["O1"]
    assert res.proposed_option_id == "O1"
    assert res.overnight_required is True
    discard_map = {o["option_id"]: o["discard_reasons"] for o in res.discarded}
    assert "INSUFFICIENT_SEATS" in discard_map["O2"]
    assert "FEE_CONFLICT" in discard_map["O2"]
    assert "UNVERIFIED_POLICY" in discard_map["O3"]
