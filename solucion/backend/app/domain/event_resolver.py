from dataclasses import dataclass, field
from typing import Any
from app.domain.models import CompanionSettings


@dataclass
class ResolvedSegment:
    segment_id: str
    state: str = "NO_EVENTS"
    delay_minutes: int | None = None
    new_departure: str | None = None
    gate: str | None = None
    gate_recorded_at: str | None = None
    event_id: str | None = None
    recorded_at: str | None = None


@dataclass
class EventResolution:
    segments: dict[str, ResolvedSegment] = field(default_factory=dict)
    chosen: list[dict[str, Any]] = field(default_factory=list)
    discarded: list[dict[str, Any]] = field(default_factory=list)
    blocking_reasons: list[str] = field(default_factory=list)
    affected_segment_id: str | None = None
    has_relevant_delay: bool = False
    has_gate_change: bool = False


def resolve_events(segments: list[dict[str, Any]], payload: dict[str, Any], settings: CompanionSettings) -> EventResolution:
    res = EventResolution(segments={s["segment_id"]: ResolvedSegment(s["segment_id"]) for s in segments})
    valid_by_seg = _filter_events(segments, payload, res)
    for seg in segments:
        _resolve_single_segment(seg["segment_id"], valid_by_seg, res)
    _finalize_anomalies(res, settings)
    return res


def _filter_events(segments: list[dict[str, Any]], payload: dict[str, Any], res: EventResolution) -> dict[str, dict[str, list[dict[str, Any]]]]:
    degraded = set(payload.get("_meta", {}).get("sources_degraded", []))
    dep_map = {s["segment_id"]: s.get("scheduled_departure", "00:00") for s in segments}
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = {s["segment_id"]: {"valid": [], "deg": []} for s in segments}
    for ev in payload.get("events", []):
        _classify_event(ev, (degraded, dep_map, grouped), res)
    return grouped


def _classify_event(ev: dict[str, Any], ctx: tuple[set[str], dict[str, str], dict[str, Any]], res: EventResolution) -> None:
    degraded, dep_map, grouped = ctx
    sid = str(ev.get("segment_id", ""))
    if sid not in dep_map:
        return res.discarded.append({"event_id": ev.get("event_id"), "reason": "UNKNOWN_SEGMENT"})
    if ev.get("source") in degraded:
        grouped[sid]["deg"].append(ev)
        return res.discarded.append({"event_id": ev.get("event_id"), "reason": "SOURCE_DEGRADED"})
    if _is_consistent_event(ev, dep_map[sid], res):
        grouped[sid]["valid"].append(ev)


def _is_consistent_event(ev: dict[str, Any], sched_dep: str, res: EventResolution) -> bool:
    etype = str(ev.get("type", ""))
    if etype not in ("DELAY", "GATE_CHANGE", "STATUS"):
        return _record_block(ev, "UNSUPPORTED_EVENT_TYPE", res)
    if etype == "DELAY" and not _check_delay_math(ev, sched_dep):
        return _record_block(ev, "INCONSISTENT_DELAY", res)
    return True


def _record_block(ev: dict[str, Any], reason: str, res: EventResolution) -> bool:
    res.blocking_reasons.append(reason)
    res.discarded.append({"event_id": ev.get("event_id"), "reason": reason})
    return False


def _check_delay_math(ev: dict[str, Any], sched_dep: str) -> bool:
    mins, new_dep = ev.get("delay_minutes"), ev.get("new_departure")
    if not isinstance(mins, int) or mins < 1 or not isinstance(new_dep, str):
        return False
    return ((_hhmm_to_min(sched_dep) + mins) % 1440) == _hhmm_to_min(new_dep)


def _hhmm_to_min(hhmm: str) -> int:
    parts = hhmm.split(":")
    return int(parts[0]) * 60 + int(parts[1])


def _resolve_single_segment(sid: str, grouped: dict[str, dict[str, list[dict[str, Any]]]], res: EventResolution) -> None:
    valid, seg_res = grouped[sid]["valid"], res.segments[sid]
    _apply_latest_gate(valid, seg_res, res)
    dep_events = [e for e in valid if e.get("type") in ("DELAY", "STATUS")]
    if not dep_events:
        seg_res.state = "NO_VERIFIED_INFO" if grouped[sid]["deg"] and not seg_res.gate else "NO_EVENTS"
        return None
    _apply_departure_precedence(dep_events, seg_res, res)


def _apply_latest_gate(valid: list[dict[str, Any]], seg_res: ResolvedSegment, res: EventResolution) -> None:
    gates = sorted([e for e in valid if e.get("type") == "GATE_CHANGE"], key=lambda x: str(x.get("recorded_at", "")))
    if not gates:
        return None
    win = gates[-1]
    seg_res.gate, seg_res.gate_recorded_at = str(win.get("gate")), str(win.get("recorded_at"))
    res.has_gate_change = True
    res.chosen.append({"event_id": win.get("event_id"), "segment_id": seg_res.segment_id, "type": "GATE_CHANGE"})


def _apply_departure_precedence(dep_events: list[dict[str, Any]], seg_res: ResolvedSegment, res: EventResolution) -> None:
    ordered = sorted(dep_events, key=lambda x: str(x.get("recorded_at", "")))
    tied = [e for e in ordered if e.get("recorded_at") == ordered[-1].get("recorded_at")]
    if len({_assertion_kind(e) for e in tied}) > 1:
        seg_res.state = "CONFLICT"
        return res.blocking_reasons.append("SOURCE_CONFLICT")
    _set_winning_departure(ordered[-1], seg_res, res)


def _assertion_kind(ev: dict[str, Any]) -> str:
    return "DELAY" if ev.get("type") == "DELAY" else str(ev.get("status", "STATUS"))


def _set_winning_departure(win: dict[str, Any], seg_res: ResolvedSegment, res: EventResolution) -> None:
    seg_res.event_id, seg_res.recorded_at = str(win.get("event_id")), str(win.get("recorded_at"))
    res.chosen.append({"event_id": seg_res.event_id, "segment_id": seg_res.segment_id, "type": win.get("type")})
    if win.get("type") != "DELAY":
        seg_res.state = "ON_TIME" if win.get("status") == "ON_TIME" else "NO_EVENTS"
        return None
    seg_res.state, seg_res.delay_minutes, seg_res.new_departure = "DELAYED", int(win["delay_minutes"]), str(win["new_departure"])


def _finalize_anomalies(res: EventResolution, settings: CompanionSettings) -> None:
    min_d = settings.relevant_delay_min_minutes
    delayed = [sid for sid, s in res.segments.items() if s.state == "DELAYED" and (s.delay_minutes or 0) >= min_d]
    if len(delayed) > 1:
        res.blocking_reasons.append("MULTIPLE_AFFECTED_SEGMENTS")
    elif len(delayed) == 1:
        res.affected_segment_id, res.has_relevant_delay = delayed[0], True
