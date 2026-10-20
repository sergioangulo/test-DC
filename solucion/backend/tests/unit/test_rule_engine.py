from app.adapters.mock_tools import BASE_POLICY
from app.domain.models import CompanionSettings
from app.domain.rule_engine import evaluate_policy


def test_evaluates_base_case_rules_and_pending_approval_state():
    variables = {
        "delay_minutes": 160,
        "international": True,
        "missed_connection": True,
        "compensation_requested": False,
        "group_includes_minor": True,
    }
    eval_res = evaluate_policy(BASE_POLICY, variables, CompanionSettings())
    results = {r["rule_id"]: r["result"] for r in eval_res.rules}
    assert results == {
        "R1": "FALSE",
        "R2": "FALSE",
        "R3": "TRUE",
        "R4": "FALSE",
        "R5": "TRUE",
    }
    assert eval_res.policy_broken is True
    assert eval_res.decision_state == "PENDIENTE_APROBACION"
    assert "REBOOK_NO_FEE" in eval_res.granted_entitlements


def test_evaluates_automatic_and_informative_and_kleene_unknown():
    adult_vars = {
        "delay_minutes": 160,
        "international": True,
        "missed_connection": True,
        "compensation_requested": False,
        "group_includes_minor": False,
    }
    auto_res = evaluate_policy(BASE_POLICY, adult_vars, CompanionSettings())
    assert auto_res.decision_state == "AUTOMATICA"

    info_vars = {**adult_vars, "delay_minutes": 30, "missed_connection": False}
    info_res = evaluate_policy(BASE_POLICY, info_vars, CompanionSettings())
    assert info_res.policy_broken is False
    assert info_res.decision_state == "INFORMATIVA"

    unknown_vars = {**adult_vars, "missed_connection": None}
    unk_res = evaluate_policy(BASE_POLICY, unknown_vars, CompanionSettings())
    assert unk_res.decision_state == "BLOQUEADA"


def test_minor_without_policy_approval_rule_is_automatic():
    policy_without_r5 = {
        **BASE_POLICY,
        "rules": [r for r in BASE_POLICY["rules"] if r["rule_id"] != "R5"],
    }
    minor_vars = {
        "delay_minutes": 160,
        "international": True,
        "missed_connection": True,
        "compensation_requested": False,
        "group_includes_minor": True,
    }
    res = evaluate_policy(policy_without_r5, minor_vars, CompanionSettings())
    assert res.policy_broken is True
    assert res.requires_human_approval is False
    assert res.decision_state == "AUTOMATICA"

