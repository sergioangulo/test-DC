from app.adapters.mock_tools import MockToolsAdapter
from app.application.companion_service import DisruptionCompanionService
from app.domain.models import CompanionSettings
from app.domain.ports import FixedClock, InMemoryDecisionStore


def _make_service(scenario: str = "BASE_TC01") -> DisruptionCompanionService:
    tools = MockToolsAdapter(scenario)
    return DisruptionCompanionService(tools, FixedClock("2026-09-15T11:02:47Z"), InMemoryDecisionStore())


def test_evaluate_base_case_tc01_returns_pending_approval_and_o1():
    svc = _make_service("BASE_TC01")
    view = svc.evaluate_trip("ABC123")
    assert view["booking_id"] == "ABC123"
    assert view["holder_first_name"] == "Ana"
    assert view["decision_state"] == "PENDIENTE_APROBACION"
    assert view["proposed_option_id"] == "O1"
    assert [o["option_id"] for o in view["options"]] == ["O1"]
    assert view["actions"][0]["effect"] == "CREATE_HUMAN_CASE"

    res = svc.accept_option("ABC123", "O1", view["decision_id"])
    assert res["outcome"] == "HUMAN_CASE_CREATED"
    assert res["human_case"]["case_id"] == "HC-4471"


def test_evaluate_and_accept_automatic_rebooking_tc07_and_timeout_tc14():
    svc = _make_service("ADULTOS_AUTOMATICO_TC07")
    view = svc.evaluate_trip("ABC123")
    assert view["decision_state"] == "AUTOMATICA"
    assert view["actions"][0]["effect"] == "CREATE_REBOOKING"

    res = svc.accept_option("ABC123", "O1", view["decision_id"])
    assert res["outcome"] == "REBOOKING_CREATED"
    assert res["operation"]["request_id"] == "RBK-88231"

    dup = svc.accept_option("ABC123", "O1", view["decision_id"])
    assert dup["outcome"] == "EXISTING_REQUEST"

    svc_timeout = _make_service("UPSTREAM_TIMEOUT_TC14")
    v_to = svc_timeout.evaluate_trip("ABC123")
    res_to = svc_timeout.accept_option("ABC123", "O1", v_to["decision_id"])
    assert res_to["outcome"] == "HUMAN_CASE_CREATED"
    assert res_to["retries"] == 2
