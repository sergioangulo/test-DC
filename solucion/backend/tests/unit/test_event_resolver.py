from app.domain.event_resolver import resolve_events
from app.domain.models import CompanionSettings


def test_excludes_degraded_source_and_resolves_base_delay():
    segments = [
        {"segment_id": "S1", "scheduled_departure": "14:30"},
        {"segment_id": "S2", "scheduled_departure": "19:05"},
    ]
    payload = {
        "events": [
            {
                "event_id": "E-1001",
                "segment_id": "S1",
                "type": "DELAY",
                "delay_minutes": 160,
                "new_departure": "17:10",
                "source": "OPS_CORE",
                "recorded_at": "2026-09-15T10:48:00Z",
            },
            {
                "event_id": "E-1007",
                "segment_id": "S1",
                "type": "GATE_CHANGE",
                "gate": "24",
                "source": "AIRPORT_FEED",
                "recorded_at": "2026-09-15T10:55:00Z",
            },
            {
                "event_id": "E-1012",
                "segment_id": "S1",
                "type": "STATUS",
                "status": "ON_TIME",
                "source": "MONITORING_FEED",
                "recorded_at": "2026-09-15T10:40:00Z",
            },
        ],
        "_meta": {"retrieved_at": "2026-09-15T11:02:33Z", "sources_degraded": ["MONITORING_FEED"]},
    }
    res = resolve_events(segments, payload, CompanionSettings())
    s1 = res.segments["S1"]
    assert s1.state == "DELAYED"
    assert s1.delay_minutes == 160
    assert s1.gate == "24"
    assert any(d["event_id"] == "E-1012" and d["reason"] == "SOURCE_DEGRADED" for d in res.discarded)
    assert res.segments["S2"].state == "NO_EVENTS"
    assert res.blocking_reasons == []


def test_detects_source_conflict_and_only_degraded():
    segments = [{"segment_id": "S1", "scheduled_departure": "14:30"}]
    conflict_payload = {
        "events": [
            {
                "event_id": "E-1",
                "segment_id": "S1",
                "type": "DELAY",
                "delay_minutes": 160,
                "new_departure": "17:10",
                "source": "OPS_CORE",
                "recorded_at": "2026-09-15T10:48:00Z",
            },
            {
                "event_id": "E-2",
                "segment_id": "S1",
                "type": "STATUS",
                "status": "ON_TIME",
                "source": "AIRPORT_FEED",
                "recorded_at": "2026-09-15T10:48:00Z",
            },
        ],
        "_meta": {"retrieved_at": "2026-09-15T11:02:33Z", "sources_degraded": []},
    }
    res = resolve_events(segments, conflict_payload, CompanionSettings())
    assert "SOURCE_CONFLICT" in res.blocking_reasons
    assert res.segments["S1"].state == "CONFLICT"

    degraded_only = {
        "events": [conflict_payload["events"][1]],
        "_meta": {"retrieved_at": "2026-09-15T11:02:33Z", "sources_degraded": ["AIRPORT_FEED"]},
    }
    res_deg = resolve_events(segments, degraded_only, CompanionSettings())
    assert res_deg.segments["S1"].state == "NO_VERIFIED_INFO"
