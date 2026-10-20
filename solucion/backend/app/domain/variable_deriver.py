from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
from app.domain.event_resolver import EventResolution
from app.domain.models import CompanionSettings, has_minor_in_group


@dataclass
class DerivedVariables:
    values: dict[str, Any] = field(default_factory=dict)
    records: list[dict[str, Any]] = field(default_factory=list)
    connection_margin_minutes: int | None = None
    mct_provided: bool = False


def derive_variables(trip: dict[str, Any], res: EventResolution, settings: CompanionSettings) -> DerivedVariables:
    out = DerivedVariables()
    minor_val = has_minor_in_group(trip.get("passengers", []))
    _add_var(out, "group_includes_minor", (minor_val, "DERIVADA", ["CHILD -> true, solo ADULT -> false"]))
    _add_var(out, "compensation_requested", (False, "DATO", ["false por defecto en evaluacion"]))
    if not res.affected_segment_id:
        return out
    _derive_segment_vars(trip["segments"], res, (settings, out))
    return out


def _add_var(out: DerivedVariables, name: str, spec: tuple[Any, str, list[str]]) -> None:
    value, origin, assumptions = spec
    out.values[name] = value
    out.records.append({"name": name, "value": value, "origin": origin, "assumptions": assumptions})


def _derive_segment_vars(segments: list[dict[str, Any]], res: EventResolution, ctx: tuple[CompanionSettings, DerivedVariables]) -> None:
    idx = next(i for i, s in enumerate(segments) if s["segment_id"] == res.affected_segment_id)
    seg, s_res = segments[idx], res.segments[str(res.affected_segment_id)]
    delay = s_res.delay_minutes or 0
    _add_var(ctx[1], "delay_minutes", (delay, "DATO", [f"evento {s_res.event_id}"]))
    new_arr_dt = _compute_new_arrival(seg, delay, ctx[1])
    _compute_international(seg, ctx[0], ctx[1])
    _compute_missed_connection(new_arr_dt, segments[idx + 1] if idx + 1 < len(segments) else None, ctx)


def _compute_new_arrival(seg: dict[str, Any], delay: int, out: DerivedVariables) -> datetime:
    dep_dt = datetime.fromisoformat(f"{seg['date']}T{seg['scheduled_departure']}")
    arr_dt = datetime.fromisoformat(f"{seg['date']}T{seg['scheduled_arrival']}")
    if arr_dt < dep_dt:
        arr_dt += timedelta(days=1)
    new_arr = arr_dt + timedelta(minutes=delay)
    _add_var(out, "new_arrival", (new_arr.strftime("%Y-%m-%dT%H:%M"), "DERIVADA", ["A1: retraso se propaga integro"]))
    return new_arr


def _compute_international(seg: dict[str, Any], settings: CompanionSettings, out: DerivedVariables) -> None:
    c_orig = settings.airport_countries.get(str(seg.get("origin", "")))
    c_dest = settings.airport_countries.get(str(seg.get("destination", "")))
    val = (c_orig != c_dest) if (c_orig and c_dest) else None
    _add_var(out, "international", (val, "DERIVADA", ["tabla IATA versionada SCL/LIM/MEX"]))


def _compute_missed_connection(new_arr: datetime, next_seg: dict[str, Any] | None, ctx: tuple[CompanionSettings, DerivedVariables]) -> None:
    settings, out = ctx
    if not next_seg:
        return _add_var(out, "missed_connection", (False, "DERIVADA", ["ultimo segmento sin conexion"]))
    next_dep = datetime.fromisoformat(f"{next_seg['date']}T{next_seg['scheduled_departure']}")
    margin = int((next_dep - new_arr).total_seconds() // 60)
    out.connection_margin_minutes = margin
    hub = str(next_seg.get("origin", ""))
    out.mct_provided = hub in settings.min_connection_minutes
    _set_missed_value(margin, settings.min_connection_minutes.get(hub, 0), out)


def _set_missed_value(margin: int, mct: int, out: DerivedVariables) -> None:
    assumptions = ["A1: retraso integro", "A2: MCT supuesto 0 no provisto", "A3: siguiente vuelo no se retiene"]
    if margin < mct:
        return _add_var(out, "missed_connection", (True, "DERIVADA", assumptions))
    val = False if (out.mct_provided or margin >= 45) else None
    _add_var(out, "missed_connection", (val, "DERIVADA", assumptions))
