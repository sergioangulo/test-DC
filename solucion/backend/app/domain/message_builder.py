from dataclasses import dataclass, field
from typing import Any

FORBIDDEN_CLAIMS = ("tu conexión está segura", "llegarás a tiempo", "ya está cambiado", "hotel pagado")


@dataclass(frozen=True)
class MessageContext:
    decision_state: str | None
    affected_flight: str | None
    delay_minutes: int | None
    new_departure: str | None
    gate: str | None
    gate_time: str | None
    missed_connection: bool | None
    policy_version: str | None
    proposed_option: dict[str, Any] | None
    overnight_required: bool
    minor_approval_rule_id: str | None
    blocking_reasons: list[str]
    no_option_reason: str | None


@dataclass
class MessageBundle:
    messages: list[dict[str, Any]] = field(default_factory=list)
    alerts: list[dict[str, str]] = field(default_factory=list)
    refund_notice: dict[str, Any] | None = None
    messages_blocked: int = 0


def build_messages(ctx: MessageContext) -> MessageBundle:
    bundle = MessageBundle()
    _append_event_messages(ctx, bundle)
    _append_option_and_step_messages(ctx, bundle)
    _validate_bundle(bundle, ctx.policy_version)
    return bundle


def _append_event_messages(ctx: MessageContext, bundle: MessageBundle) -> None:
    if ctx.blocking_reasons:
        msg = "Detectamos información operacional en conflicto o incompleta. Una persona revisará tu vuelo."
        _push_msg(bundle, ("MSG_BLOCKING", "WARNING", msg, ctx.blocking_reasons, None), "CRITICAL")
    if ctx.delay_minutes:
        msg = f"Tu vuelo {ctx.affected_flight} presenta un retraso validado de {ctx.delay_minutes} min (nueva salida {ctx.new_departure})."
        _push_msg(bundle, ("MSG_DELAY", "INFO", msg, ["E-DELAY"], None), "WARNING")
    if ctx.gate:
        msg = f"Puerta {ctx.gate} informada a las {ctx.gate_time}. Confirma siempre en pantallas del aeropuerto."
        _push_msg(bundle, ("MSG_GATE", "INFO", msg, ["E-GATE"], None), "INFO")


def _append_option_and_step_messages(ctx: MessageContext, bundle: MessageBundle) -> None:
    if ctx.missed_connection is True:
        msg = "Estimación: el retraso compromete tu conexión en el aeropuerto de escala (sujeto a tiempo mínimo de conexión)."
        _push_msg(bundle, ("MSG_CONN", "ESTIMATE", msg, ["DERIVED_CONN"], None), "WARNING")
    if ctx.proposed_option and ctx.policy_version:
        _append_proposal_messages(ctx, bundle)
    elif ctx.no_option_reason:
        msg = "Las opciones disponibles no tienen asientos para todo tu grupo junto. Una persona puede ayudarte con otras alternativas."
        _push_msg(bundle, ("MSG_NO_OPT", "WARNING", msg, [ctx.no_option_reason], ctx.policy_version), "WARNING")


def _append_proposal_messages(ctx: MessageContext, bundle: MessageBundle) -> None:
    opt = ctx.proposed_option or {}
    text = _proposal_text(opt)
    _push_msg(bundle, ("MSG_PROPOSAL", "NEXT_STEP", text, [str(opt.get("option_id"))], ctx.policy_version), None)
    if ctx.minor_approval_rule_id and ctx.decision_state == "PENDIENTE_APROBACION":
        _push_msg(bundle, ("MSG_MINOR", "INFO", "Tu grupo incluye a un menor: esta decisión necesita la validación de uno de nuestros agentes.", [ctx.minor_approval_rule_id], ctx.policy_version), None)
    if ctx.overnight_required:
        _push_msg(bundle, ("MSG_OVERNIGHT", "INFO", "Tu nueva salida es al día siguiente: podrías tener derecho a asistencia; un agente lo confirmará.", ["OVERNIGHT"], None), "INFO")
    _push_msg(bundle, ("MSG_REFUND", "INFO", "Si prefieres no viajar, un agente puede revisar contigo las alternativas.", ["O3"], None), None)
    bundle.refund_notice = bundle.messages[-1]


def _proposal_text(opt: dict[str, Any]) -> str:
    route = f"{opt.get('flight_number')} el {opt.get('date')} a las {opt.get('departure')}"
    return f"Te proponemos: Cambiar tu vuelo a {route} {_fare_phrase(opt)} (sujeto a disponibilidad)."


def _fare_phrase(opt: dict[str, Any]) -> str:
    fare = opt.get("fare_difference") or 0
    if fare == 0:
        return "sin costo adicional"
    return f"con una diferencia tarifaria de {fare} {opt.get('currency') or ''}".replace("  ", " ").strip()


def _push_msg(bundle: MessageBundle, spec: tuple[str, str, str, list[str], str | None], severity: str | None) -> None:
    mid, kind, text, refs, pol = spec
    bundle.messages.append({"message_id": mid, "kind": kind, "text": text, "evidence_refs": refs, "policy_ref": pol})
    if severity:
        bundle.alerts.append({"code": mid, "severity": severity, "text": text})


def _validate_bundle(bundle: MessageBundle, active_policy: str | None) -> None:
    valid: list[dict[str, Any]] = []
    for msg in bundle.messages:
        if validate_message(msg, active_policy):
            valid.append(msg)
        else:
            bundle.messages_blocked += 1
    bundle.messages = valid


def validate_message(msg: dict[str, Any], active_policy: str | None) -> bool:
    text = str(msg.get("text", "")).lower()
    if not text or any(bad in text for bad in FORBIDDEN_CLAIMS):
        return False
    if not msg.get("evidence_refs"):
        return False
    if msg.get("kind") == "NEXT_STEP":
        return bool(active_policy and msg.get("policy_ref") == active_policy)
    return True
