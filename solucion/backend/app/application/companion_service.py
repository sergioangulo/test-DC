import hashlib
import uuid
from dataclasses import asdict
from typing import Any
from app.domain.event_resolver import EventResolution, resolve_events
from app.domain.message_builder import MessageContext, build_messages
from app.domain.models import CompanionSettings, ReducedTripContext, extract_holder_first_name
from app.domain.option_filter import OptionFilterContext, OptionFilterResult, filter_options
from app.domain.ports import ClockPort, InMemoryDecisionStore, RebookingCommand, ToolsPort
from app.domain.rule_engine import PolicyEvaluation, evaluate_policy
from app.domain.variable_deriver import DerivedVariables, derive_variables


class DisruptionCompanionService:
    def __init__(self, tools: ToolsPort, clock: ClockPort, store: InMemoryDecisionStore | None = None) -> None:
        self.tools = tools
        self.clock = clock
        self.store = store or InMemoryDecisionStore()
        self.settings = CompanionSettings()

    def evaluate_trip(self, booking_id: str) -> dict[str, Any]:
        trip = self.tools.get_trip_context(booking_id)
        seg_ids = [s["segment_id"] for s in trip.get("segments", [])]
        ev_res = resolve_events(trip["segments"], self.tools.get_operational_events(seg_ids), self.settings)
        derived = derive_variables(trip, ev_res, self.settings)
        pol_res, opt_res, state = self._run_policy_and_options(trip, ev_res, derived)
        return self._assemble_and_save(trip, (ev_res, derived, pol_res, opt_res, state))

    def _run_policy_and_options(self, trip: dict[str, Any], ev_res: EventResolution, derived: DerivedVariables) -> tuple[PolicyEvaluation | None, OptionFilterResult, str | None]:
        if ev_res.blocking_reasons:
            return None, OptionFilterResult(), "BLOQUEADA"
        if not ev_res.has_relevant_delay:
            return None, OptionFilterResult(), ("INFORMATIVA" if ev_res.has_gate_change else None)
        pol = evaluate_policy(self.tools.get_policy_rules("DELAY"), derived.values, self.settings)
        if not pol.policy_broken or pol.decision_state == "BLOQUEADA":
            return pol, OptionFilterResult(), pol.decision_state
        return self._fetch_and_filter_options(trip, (ev_res, derived, pol))

    def _fetch_and_filter_options(self, trip: dict[str, Any], eval_tuple: tuple[EventResolution, DerivedVariables, PolicyEvaluation]) -> tuple[PolicyEvaluation, OptionFilterResult, str]:
        ev_res, derived, pol = eval_tuple
        raw_opts = self.tools.get_eligible_options(ReducedTripContext.from_trip(trip))
        f_ctx = OptionFilterContext(len(trip["passengers"]), trip["segments"], ev_res.affected_segment_id, derived.values, pol, self.clock.now_iso())
        opt_res = filter_options(raw_opts, f_ctx, self.settings)
        return pol, opt_res, ("BLOQUEADA" if not opt_res.viable else pol.decision_state)

    def _assemble_and_save(self, trip: dict[str, Any], parts: tuple[Any, ...]) -> dict[str, Any]:
        ev_res, derived, pol, opt_res, state = parts
        msg_bundle = build_messages(self._build_msg_context(trip, parts))
        actions = _build_offered_actions(state, opt_res, ev_res.blocking_reasons)
        view = _compose_trip_view(trip, self.clock.now_iso(), (ev_res, derived, pol, opt_res, state, msg_bundle, actions))
        self.store.save_decision({**view, "_passenger_ids": [p["passenger_id"] for p in trip.get("passengers", [])]})
        return view

    def _build_msg_context(self, trip: dict[str, Any], parts: tuple[Any, ...]) -> MessageContext:
        ev_res, derived, pol, opt_res, state = parts
        aff_id = ev_res.affected_segment_id or (trip["segments"][0]["segment_id"] if trip.get("segments") else "")
        seg_res = ev_res.segments.get(aff_id)
        flight = next((s["flight_number"] for s in trip.get("segments", []) if s["segment_id"] == aff_id), None)
        prop = opt_res.viable[0] if opt_res.viable else None
        return _create_msg_ctx((state, flight, seg_res), (derived, pol, prop), (opt_res, ev_res))

    def accept_option(self, booking_id: str, option_id: str, decision_id: str) -> dict[str, Any]:
        rec = self.store.get_decision(decision_id)
        if not rec or rec.get("booking_id") != booking_id:
            raise KeyError(decision_id)
        opt = next((o for o in rec.get("options", []) if o["option_id"] == option_id), None)
        if not opt and rec.get("decision_state") != "BLOQUEADA":
            raise ValueError("OPTION_NOT_OFFERED")
        if rec.get("decision_state") == "AUTOMATICA" and opt:
            return self._execute_rebooking(rec, opt)
        return self._escalate_to_human(rec, opt, "POLICY_APPROVAL_REQUIRED" if rec.get("decision_state") == "PENDIENTE_APROBACION" else "BLOCKING_ANOMALY")

    def _execute_rebooking(self, rec: dict[str, Any], opt: dict[str, Any]) -> dict[str, Any]:
        idem_key = _compute_idempotency_key(rec["booking_id"], opt)
        if idem_key in self.store.operations:
            return _rebook_response("EXISTING_REQUEST", self.store.operations[idem_key], 0)
        cmd = RebookingCommand(str(opt["option_id"]), idem_key, str(rec["booking_id"]), tuple(rec.get("_passenger_ids", [])))
        status, payload, retries = self._call_rebooking_with_retries(cmd)
        if status == 503:
            return {**self._escalate_to_human(rec, opt, "UPSTREAM_INDETERMINATE"), "retries": retries}
        self.store.operations[idem_key] = payload
        return _rebook_response("REBOOKING_CREATED" if status == 201 else "EXISTING_REQUEST", payload, retries)

    def _call_rebooking_with_retries(self, cmd: RebookingCommand) -> tuple[int, dict[str, Any], int]:
        status, payload = self.tools.create_rebooking_request(cmd)
        retries = 0
        while status == 503 and retries < self.settings.rebook_max_retries:
            retries += 1
            status, payload = self.tools.create_rebooking_request(cmd)
        return status, payload, retries

    def _escalate_to_human(self, rec: dict[str, Any], opt: dict[str, Any] | None, reason: str) -> dict[str, Any]:
        dedup_key = f"{rec['booking_id']}:{reason}:{rec['decision_id']}"
        if dedup_key in self.store.human_cases:
            return {"outcome": "EXISTING_CASE", "operation": None, "human_case": self.store.human_cases[dedup_key], "retries": 0, "message": {"text": "Tu caso ya se encuentra asignado a un especialista."}}
        evidence = {"booking_id": rec["booking_id"], "decision_id": rec["decision_id"], "selected_option_id": opt["option_id"] if opt else None, "policy_version": (rec.get("policy") or {}).get("version")}
        _, hc_payload = self.tools.create_human_case(reason, evidence)
        self.store.human_cases[dedup_key] = hc_payload
        return {"outcome": "HUMAN_CASE_CREATED", "operation": None, "human_case": hc_payload, "retries": 0, "message": {"text": f"Hemos derivado tu solicitud a uno de nuestros ejecutivos de soporte (tiempo estimado de atención: {hc_payload['sla_minutes']} minutos). Tu reserva aún no se modifica."}}


def _create_msg_ctx(head: tuple[Any, ...], mid: tuple[Any, ...], tail: tuple[Any, ...]) -> MessageContext:
    state, flight, seg_res = head
    derived, pol, prop = mid
    opt_res, ev_res = tail
    d_min = seg_res.delay_minutes if seg_res else None
    n_dep = seg_res.new_departure if seg_res else None
    gate, g_at = (seg_res.gate if seg_res else None), (seg_res.gate_recorded_at if seg_res else None)
    minor_rule = _find_minor_approval_rule(pol)
    return MessageContext(state, flight, d_min, n_dep, gate, g_at, derived.values.get("missed_connection"), pol.version if pol else None, prop, opt_res.overnight_required, minor_rule, ev_res.blocking_reasons, opt_res.no_option_reason)


def _find_minor_approval_rule(pol: PolicyEvaluation | None) -> str | None:
    if not pol:
        return None
    for rule in pol.rules:
        if rule.get("result") == "TRUE" and rule.get("requires_human_approval") is True and "group_includes_minor" in str(rule.get("condition", "")):
            return str(rule.get("rule_id"))
    return None


def _rebook_response(outcome: str, payload: dict[str, Any], retries: int) -> dict[str, Any]:
    text = "Solicitud registrada, pendiente de confirmación, sujeta a disponibilidad." if outcome == "REBOOKING_CREATED" else "Ya existe una solicitud en curso para esta opción."
    return {"outcome": outcome, "operation": payload, "human_case": None, "retries": retries, "message": {"text": text}}


def _compute_idempotency_key(booking_id: str, opt: dict[str, Any]) -> str:
    raw = f"{booking_id}:{opt.get('flight_number')}:{opt.get('date')}:{opt.get('departure')}:{opt.get('policy_ref')}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def _build_offered_actions(state: str | None, opt_res: OptionFilterResult, blocking: list[str]) -> list[dict[str, Any]]:
    if state in (None, "INFORMATIVA"):
        return []
    if opt_res.proposed_option_id:
        eff = "CREATE_REBOOKING" if state == "AUTOMATICA" else "CREATE_HUMAN_CASE"
        lbl = "Aceptar esta opción (cambio sin costo)" if eff == "CREATE_REBOOKING" else "Aceptar opción y contactar a un agente de soporte"
        return [{"action_id": "ACT_ACCEPT", "kind": "ACCEPT_OPTION", "option_id": opt_res.proposed_option_id, "effect": eff, "label": lbl}]
    reason = blocking[0] if blocking else (opt_res.no_option_reason or "OTHER_HELP")
    return [{"action_id": "ACT_HUMAN", "kind": "OPEN_HUMAN_CASE", "option_id": "MANUAL", "effect": "CREATE_HUMAN_CASE", "label": "Contactar a un ejecutivo", "reason": reason}]


def _compose_trip_view(trip: dict[str, Any], now_iso: str, parts: tuple[Any, ...]) -> dict[str, Any]:
    ev_res, derived, pol, opt_res, state, msg_bundle, actions = parts
    segments_view = [{**s, **asdict(ev_res.segments[s["segment_id"]])} for s in trip.get("segments", [])]
    anom = bool(ev_res.has_relevant_delay or ev_res.has_gate_change or ev_res.blocking_reasons)
    holder = extract_holder_first_name(trip.get("passengers", []))
    base = {"decision_id": str(uuid.uuid4()), "booking_id": trip["booking_id"], "generated_at": now_iso, "anomaly_detected": anom, "decision_state": state, "holder_first_name": holder, "passenger_count": len(trip.get("passengers", []))}
    extra = {"completeness": trip.get("_meta", {}).get("completeness", "COMPLETE"), "missing_fields": trip.get("_meta", {}).get("missing_fields", []), "segments": segments_view, "chosen_events": ev_res.chosen, "discarded_events": ev_res.discarded, "blocking_reasons": ev_res.blocking_reasons, "derived_variables": derived.records, "policy": asdict(pol) if pol else None, "options": opt_res.viable, "discarded_options": opt_res.discarded, "proposed_option_id": opt_res.proposed_option_id, "offer_deadline": opt_res.offer_deadline, "overnight_required": opt_res.overnight_required, "alerts": msg_bundle.alerts, "messages": msg_bundle.messages, "refund_notice": msg_bundle.refund_notice, "actions": actions}
    return {**base, **extra}
