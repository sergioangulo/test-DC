from dataclasses import dataclass, field
from typing import Any
from app.domain.models import CompanionSettings

ALLOWED_VARS = {
    "delay_minutes",
    "international",
    "missed_connection",
    "compensation_requested",
    "group_includes_minor",
}


@dataclass
class PolicyEvaluation:
    version: str
    superseded_versions: list[str]
    rules: list[dict[str, Any]] = field(default_factory=list)
    granted_entitlements: list[str] = field(default_factory=list)
    policy_broken: bool = False
    requires_human_approval: bool = False
    has_rule_error: bool = False
    has_blocking_unknown: bool = False
    decision_state: str = "INFORMATIVA"


def evaluate_policy(policy: dict[str, Any], variables: dict[str, Any], settings: CompanionSettings) -> PolicyEvaluation:
    sup = list(policy.get("_meta", {}).get("superseded_versions", []))
    out = PolicyEvaluation(version=str(policy.get("version", "")), superseded_versions=sup)
    if not policy.get("rules"):
        out.has_rule_error, out.decision_state = True, "BLOQUEADA"
        return out
    for rule in policy["rules"]:
        _evaluate_single_rule(rule, variables, (settings, out))
    out.decision_state = _resolve_decision_state(out, variables)
    return out


def _evaluate_single_rule(rule: dict[str, Any], variables: dict[str, Any], ctx: tuple[CompanionSettings, PolicyEvaluation]) -> None:
    settings, out = ctx
    cond = str(rule.get("condition", ""))
    res_str = _eval_condition_safe(cond, variables, settings)
    rights = [str(r) for r in rule.get("entitlements", [])]
    approval = rule.get("requires_human_approval")
    out.rules.append({"rule_id": rule.get("rule_id"), "condition": cond, "result": res_str, "entitlements": rights, "requires_human_approval": approval})
    _accumulate_rule_effects(res_str, (rights, approval), ctx)


def _accumulate_rule_effects(res_str: str, rule_meta: tuple[list[str], Any], ctx: tuple[CompanionSettings, PolicyEvaluation]) -> None:
    settings, out = ctx
    rights, approval = rule_meta
    if res_str == "RULE_ERROR":
        out.has_rule_error = True
    elif res_str == "UNKNOWN" and any(r in settings.remedy_rights for r in rights):
        out.has_blocking_unknown = True
    elif res_str == "TRUE":
        _apply_matched_rule(rights, approval, ctx)


def _apply_matched_rule(rights: list[str], approval: Any, ctx: tuple[CompanionSettings, PolicyEvaluation]) -> None:
    settings, out = ctx
    out.granted_entitlements.extend([r for r in rights if r not in out.granted_entitlements])
    if any(r in settings.remedy_rights for r in rights):
        out.policy_broken = True
    if not isinstance(approval, bool):
        out.has_rule_error = True
    elif approval:
        out.requires_human_approval = True


def _resolve_decision_state(out: PolicyEvaluation, variables: dict[str, Any]) -> str:
    if out.has_rule_error or out.has_blocking_unknown:
        return "BLOQUEADA"
    if not out.policy_broken:
        return "INFORMATIVA"
    if variables.get("group_includes_minor") is None:
        return "BLOQUEADA"
    return "PENDIENTE_APROBACION" if out.requires_human_approval else "AUTOMATICA"


def _eval_condition_safe(cond: str, variables: dict[str, Any], settings: CompanionSettings) -> str:
    if not cond or len(cond) > settings.parser_max_chars:
        return "RULE_ERROR"
    try:
        val = _eval_or_branches(cond.strip(), variables)
        return "UNKNOWN" if val is None else ("TRUE" if val else "FALSE")
    except ValueError:
        return "RULE_ERROR"


def _eval_or_branches(expr: str, variables: dict[str, Any]) -> bool | None:
    parts = [p.strip() for p in expr.split(" OR ")]
    vals = [_eval_and_branches(p, variables) for p in parts]
    if any(v is True for v in vals):
        return True
    return None if any(v is None for v in vals) else False


def _eval_and_branches(expr: str, variables: dict[str, Any]) -> bool | None:
    parts = [p.strip() for p in expr.split(" AND ")]
    vals = [_eval_atom(p, variables) for p in parts]
    if any(v is False for v in vals):
        return False
    return None if any(v is None for v in vals) else True


def _eval_atom(atom: str, variables: dict[str, Any]) -> bool | None:
    cleaned = atom.strip().removeprefix("(").removesuffix(")").strip()
    tokens = cleaned.split()
    if len(tokens) != 3 or tokens[0] not in ALLOWED_VARS:
        raise ValueError("Invalid condition token")
    lhs = variables.get(tokens[0])
    rhs = _parse_literal(tokens[2])
    return _compare_values(lhs, tokens[1], rhs)


def _parse_literal(token: str) -> int | bool:
    if token in ("true", "false"):
        return token == "true"
    if token.lstrip("-").isdigit():
        return int(token)
    raise ValueError("Invalid literal")


def _compare_values(lhs: Any, op: str, rhs: int | bool) -> bool | None:
    if lhs is None:
        return None
    if type(lhs) is not type(rhs):
        raise ValueError("Type mismatch")
    if isinstance(rhs, bool) and op not in ("==", "EQ", "!=", "NE"):
        raise ValueError("Invalid boolean operator")
    return _apply_operator(lhs, op, rhs)


def _apply_operator(lhs: Any, op: str, rhs: Any) -> bool:
    if op in ("==", "EQ"):
        return bool(lhs == rhs)
    if op in ("!=", "NE"):
        return bool(lhs != rhs)
    order_ops = {">=": lhs >= rhs, ">": lhs > rhs, "<=": lhs <= rhs, "<": lhs < rhs}
    if op not in order_ops:
        raise ValueError("Unsupported operator")
    return bool(order_ops[op])
