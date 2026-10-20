from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any
from app.domain.models import CompanionSettings
from app.domain.rule_engine import PolicyEvaluation

CONFIDENCE_RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}


@dataclass(frozen=True)
class OptionFilterContext:
    passenger_count: int
    segments: list[dict[str, Any]]
    affected_segment_id: str | None
    variables: dict[str, Any]
    policy: PolicyEvaluation
    now_iso: str


@dataclass
class OptionFilterResult:
    viable: list[dict[str, Any]] = field(default_factory=list)
    discarded: list[dict[str, Any]] = field(default_factory=list)
    proposed_option_id: str | None = None
    offer_deadline: str | None = None
    overnight_required: bool = False
    no_option_reason: str | None = None


def filter_options(payload: dict[str, Any], ctx: OptionFilterContext, settings: CompanionSettings) -> OptionFilterResult:
    out = OptionFilterResult()
    exp_iso, ttl_expired = _compute_ttl_deadline(payload.get("_meta", {}), ctx.now_iso)
    for raw in payload.get("options", []):
        _classify_option(dict(raw), (ctx, settings, ttl_expired), out)
    out.viable.sort(key=lambda o: (CONFIDENCE_RANK.get(str(o.get("confidence")), 9), str(o.get("date", "")), str(o.get("departure", "")), str(o.get("option_id", ""))))
    _finalize_proposed_option(out, ctx, exp_iso)
    return out


def _compute_ttl_deadline(meta: dict[str, Any], now_iso: str) -> tuple[str | None, bool]:
    ret = meta.get("retrieved_at")
    ttl = meta.get("ttl_seconds")
    if not isinstance(ret, str) or not isinstance(ttl, int) or ttl <= 0:
        return None, True
    exp_dt = _parse_utc(ret) + timedelta(seconds=ttl)
    now_dt = _parse_utc(now_iso)
    return exp_dt.strftime("%Y-%m-%dT%H:%M:%SZ"), now_dt >= exp_dt


def _parse_utc(iso_str: str) -> datetime:
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00")).astimezone(timezone.utc)


def _classify_option(opt: dict[str, Any], env: tuple[OptionFilterContext, CompanionSettings, bool], out: OptionFilterResult) -> None:
    reasons = _collect_discard_reasons(opt, env)
    opt["viable"] = len(reasons) == 0
    opt["discard_reasons"] = reasons
    if opt["viable"]:
        out.viable.append(opt)
    else:
        out.discarded.append(opt)


def _collect_discard_reasons(opt: dict[str, Any], env: tuple[OptionFilterContext, CompanionSettings, bool]) -> list[str]:
    ctx, settings, ttl_expired = env
    reasons: list[str] = []
    _check_policy_and_type(opt, ctx.policy, reasons)
    if opt.get("type") == "REBOOKING":
        _check_seats_and_fee(opt, (ctx, settings), reasons)
        _check_itinerary_coherence(opt, ctx, reasons)
    if ttl_expired:
        reasons.append("EXPIRED_TTL")
    return reasons


def _check_policy_and_type(opt: dict[str, Any], pol: PolicyEvaluation, reasons: list[str]) -> None:
    if opt.get("type") != "REBOOKING":
        reasons.append("UNSUPPORTED_OPTION_TYPE")
    pref = str(opt.get("policy_ref", ""))
    if pref in pol.superseded_versions:
        reasons.append("SUPERSEDED_POLICY")
    elif pref != pol.version:
        reasons.append("UNVERIFIED_POLICY")


def _check_seats_and_fee(opt: dict[str, Any], pair: tuple[OptionFilterContext, CompanionSettings], reasons: list[str]) -> None:
    ctx, settings = pair
    seats = opt.get("seats_available")
    if not isinstance(seats, int) or seats < ctx.passenger_count:
        reasons.append("INSUFFICIENT_SEATS")
    fare = opt.get("fare_difference", 0)
    has_right = any(r in settings.change_rights for r in ctx.policy.granted_entitlements)
    if not has_right or fare != 0 or (fare > 0 and not opt.get("currency")):
        reasons.append("FEE_CONFLICT")


def _check_itinerary_coherence(opt: dict[str, Any], ctx: OptionFilterContext, reasons: list[str]) -> None:
    missed = ctx.variables.get("missed_connection")
    if missed is None:
        return reasons.append("UNCERTAIN_ITINERARY")
    target = _expected_route(ctx.segments, ctx.affected_segment_id, bool(missed))
    if not target or (opt.get("origin"), opt.get("destination")) != target:
        reasons.append("ITINERARY_MISMATCH")


def _expected_route(segments: list[dict[str, Any]], affected_id: str | None, missed: bool) -> tuple[str, str] | None:
    idx = next((i for i, s in enumerate(segments) if s["segment_id"] == affected_id), None)
    if idx is None:
        return None
    if missed and idx + 1 < len(segments):
        return str(segments[idx + 1]["origin"]), str(segments[-1]["destination"])
    return str(segments[idx]["origin"]), str(segments[idx]["destination"])


def _finalize_proposed_option(out: OptionFilterResult, ctx: OptionFilterContext, exp_iso: str | None) -> None:
    if not out.viable:
        seat_issue = any("INSUFFICIENT_SEATS" in o["discard_reasons"] for o in out.discarded)
        out.no_option_reason = "NO_OPTION_COVERS_GROUP" if seat_issue else "NO_VIABLE_OPTION"
        return None
    best = out.viable[0]
    out.proposed_option_id, out.offer_deadline = str(best["option_id"]), exp_iso
    new_arr = str(ctx.variables.get("new_arrival", ""))
    out.overnight_required = bool(ctx.variables.get("missed_connection") and new_arr and str(best.get("date", "")) > new_arr[:10])
