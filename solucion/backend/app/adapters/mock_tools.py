from copy import deepcopy
from typing import Any
from app.domain.models import ReducedTripContext
from app.domain.ports import RebookingCommand

BASE_SEGMENTS = [
    {
        "segment_id": "S1",
        "flight_number": "LA500",
        "origin": "SCL",
        "destination": "LIM",
        "date": "2026-09-15",
        "scheduled_departure": "14:30",
        "scheduled_arrival": "17:55",
        "status": "SCHEDULED",
    },
    {
        "segment_id": "S2",
        "flight_number": "LA2410",
        "origin": "LIM",
        "destination": "MEX",
        "date": "2026-09-15",
        "scheduled_departure": "19:05",
        "scheduled_arrival": "23:40",
        "status": "SCHEDULED",
    },
]

BASE_PASSENGERS = [
    {"passenger_id": "P1", "name": "Ana Prueba", "type": "ADULT", "loyalty_tier": "GOLD"},
    {"passenger_id": "P2", "name": "Lucas Prueba", "type": "CHILD", "age": 8},
]

ADULT_PASSENGERS = [
    {"passenger_id": "P1", "name": "Ana Prueba", "type": "ADULT"},
    {"passenger_id": "P2", "name": "Carlos Prueba", "type": "ADULT"},
]

BASE_EVENTS = [
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
    {
        "event_id": "E-2003",
        "segment_id": "S2",
        "type": "STATUS",
        "status": "SCHEDULED",
        "source": "OPS_CORE",
        "recorded_at": "2026-09-15T09:00:00Z",
    },
]

BASE_POLICY = {
    "scenario": "DELAY",
    "version": "POL-DELAY-2026-03",
    "effective_from": "2026-03-01",
    "rules": [
        {
            "rule_id": "R1",
            "condition": "delay_minutes >= 180",
            "entitlements": ["MEAL_VOUCHER", "REBOOK_NO_FEE"],
            "requires_human_approval": False,
        },
        {
            "rule_id": "R2",
            "condition": "delay_minutes >= 240 AND international == true",
            "entitlements": ["HOTEL_ASSISTANCE", "GROUND_TRANSPORT", "REBOOK_NO_FEE"],
            "requires_human_approval": True,
        },
        {
            "rule_id": "R3",
            "condition": "missed_connection == true",
            "entitlements": ["REBOOK_NO_FEE"],
            "requires_human_approval": False,
        },
        {
            "rule_id": "R4",
            "condition": "compensation_requested == true",
            "entitlements": ["CASH_COMPENSATION"],
            "requires_human_approval": True,
        },
        {
            "rule_id": "R5",
            "condition": "group_includes_minor == true",
            "entitlements": ["PRIORITY_HANDLING"],
            "requires_human_approval": True,
        },
    ],
    "_meta": {"superseded_versions": ["POL-DELAY-2025-11"]},
}

BASE_OPTIONS = [
    {
        "option_id": "O1",
        "type": "REBOOKING",
        "flight_number": "LA2412",
        "origin": "LIM",
        "destination": "MEX",
        "date": "2026-09-16",
        "departure": "08:15",
        "seats_available": 4,
        "fare_difference": 0,
        "currency": "CLP",
        "policy_ref": "POL-DELAY-2026-03",
        "confidence": "HIGH",
    },
    {
        "option_id": "O2",
        "type": "REBOOKING",
        "flight_number": "LA2450",
        "origin": "LIM",
        "destination": "MEX",
        "date": "2026-09-15",
        "departure": "22:30",
        "seats_available": 1,
        "fare_difference": 180000,
        "currency": "CLP",
        "policy_ref": "POL-DELAY-2026-03",
        "confidence": "MEDIUM",
    },
    {
        "option_id": "O3",
        "type": "REFUND",
        "policy_ref": "POL-REFUND-2025-09",
        "confidence": "LOW",
    },
]

SCENARIOS: dict[str, dict[str, Any]] = {
    "BASE_TC01": {
        "title": "Caso Base PDF (ABC123: retraso 160m + menor + conexión perdida)",
        "description": "S1 retrasado 160 min, E-1012 degradado excluido, R3 y R5 verdaderas, O1 viable y requiere aprobación humana por menor.",
        "passengers": BASE_PASSENGERS,
        "events": BASE_EVENTS,
        "degraded": ["MONITORING_FEED"],
        "options": BASE_OPTIONS,
        "rebook_mode": "OK",
    },
    "ADULTOS_AUTOMATICO_TC07": {
        "title": "Rebooking Automático (TC-07: dos adultos sin menor)",
        "description": "Dos pasajeros adultos con conexión perdida: R3 verdadera, R5 falsa, decisión AUTOMATICA que habilita create_rebooking_request.",
        "passengers": ADULT_PASSENGERS,
        "events": BASE_EVENTS,
        "degraded": ["MONITORING_FEED"],
        "options": BASE_OPTIONS,
        "rebook_mode": "OK",
    },
    "CONFLICTO_FUENTES_TC03": {
        "title": "Conflicto de Fuentes (TC-03: empate de timestamp entre fuentes sanas)",
        "description": "Dos fuentes activas afirman DELAY y ON_TIME en el mismo instante: bloquea decisión automática y escala a humano.",
        "passengers": BASE_PASSENGERS,
        "events": [
            BASE_EVENTS[0],
            {
                "event_id": "E-1099",
                "segment_id": "S1",
                "type": "STATUS",
                "status": "ON_TIME",
                "source": "AIRPORT_FEED",
                "recorded_at": "2026-09-15T10:48:00Z",
            },
        ],
        "degraded": [],
        "options": BASE_OPTIONS,
        "rebook_mode": "OK",
    },
    "SOLO_DEGRADADO_TC02": {
        "title": "Solo Fuente Degradada (TC-02: sin información verificada)",
        "description": "Único evento proviene de MONITORING_FEED degradada: no afirma 'a tiempo', informa 'sin información verificada'.",
        "passengers": BASE_PASSENGERS,
        "events": [BASE_EVENTS[2]],
        "degraded": ["MONITORING_FEED"],
        "options": BASE_OPTIONS,
        "rebook_mode": "OK",
    },
    "SIN_OPCION_VIABLE_TC09": {
        "title": "Sin Opción Viable para el Grupo (TC-09: solo 1 asiento para 2 pasajeros)",
        "description": "Solo existe O2 con 1 asiento y diferencia tarifaria: ninguna opción cubre al grupo y se ofrece caso humano.",
        "passengers": ADULT_PASSENGERS,
        "events": BASE_EVENTS,
        "degraded": ["MONITORING_FEED"],
        "options": [BASE_OPTIONS[1]],
        "rebook_mode": "OK",
    },
    "UPSTREAM_TIMEOUT_TC14": {
        "title": "Timeout Indeterminado 503 en Rebooking (TC-14: reintentos y escalamiento)",
        "description": "create_rebooking_request responde 503 UPSTREAM_TIMEOUT indeterminado: reintenta con misma llave y deriva a caso humano.",
        "passengers": ADULT_PASSENGERS,
        "events": BASE_EVENTS,
        "degraded": ["MONITORING_FEED"],
        "options": BASE_OPTIONS,
        "rebook_mode": "TIMEOUT_503",
    },
}


class MockToolsAdapter:
    def __init__(self, initial_scenario: str = "BASE_TC01") -> None:
        self.active_scenario = initial_scenario
        self.created_keys: set[str] = set()
        self.rebook_calls: list[str] = []

    def activate_scenario(self, scenario_id: str) -> dict[str, Any]:
        if scenario_id not in SCENARIOS:
            raise KeyError(scenario_id)
        self.active_scenario = scenario_id
        self.created_keys.clear()
        self.rebook_calls.clear()
        return self.current_scenario_meta()

    def current_scenario_meta(self) -> dict[str, Any]:
        return {
            "active_scenario_id": self.active_scenario,
            "booking_id": "ABC123",
            "clock_utc": "2026-09-15T11:02:35Z",
        }

    def list_scenarios(self) -> list[dict[str, str]]:
        return [
            {"scenario_id": sid, "booking_id": "ABC123", "title": cfg["title"], "description": cfg["description"]}
            for sid, cfg in SCENARIOS.items()
        ]

    def get_trip_context(self, booking_id: str) -> dict[str, Any]:
        if booking_id != "ABC123":
            raise KeyError(booking_id)
        cfg = SCENARIOS[self.active_scenario]
        meta = {"retrieved_at": "2026-09-15T11:02:31Z", "completeness": "PARTIAL", "missing_fields": ["change_penalty_amount"]}
        fare = {"refundable": False, "change_penalty_amount": None}
        return {"booking_id": "ABC123", "passengers": deepcopy(cfg["passengers"]), "segments": deepcopy(BASE_SEGMENTS), "fare_conditions": fare, "_meta": meta}

    def get_operational_events(self, segment_ids: list[str]) -> dict[str, Any]:
        cfg = SCENARIOS[self.active_scenario]
        filtered = [deepcopy(e) for e in cfg["events"] if e.get("segment_id") in segment_ids]
        meta = {"retrieved_at": "2026-09-15T11:02:33Z", "sources_available": ["OPS_CORE", "AIRPORT_FEED"], "sources_degraded": list(cfg["degraded"])}
        return {"events": filtered, "_meta": meta}

    def get_policy_rules(self, scenario: str) -> dict[str, Any]:
        if scenario != "DELAY":
            raise KeyError(scenario)
        return deepcopy(BASE_POLICY)

    def get_eligible_options(self, context: ReducedTripContext) -> dict[str, Any]:
        cfg = SCENARIOS[self.active_scenario]
        return {
            "options": deepcopy(cfg["options"]),
            "_meta": {"retrieved_at": "2026-09-15T11:02:35Z", "ttl_seconds": 120},
        }

    def create_rebooking_request(self, command: RebookingCommand) -> tuple[int, dict[str, Any]]:
        self.rebook_calls.append(command.idempotency_key)
        if SCENARIOS[self.active_scenario]["rebook_mode"] == "TIMEOUT_503":
            return 503, {"error": "UPSTREAM_TIMEOUT"}
        if command.idempotency_key in self.created_keys:
            return 409, {"error": "DUPLICATE_REQUEST", "existing_request_id": "RBK-88231"}
        self.created_keys.add(command.idempotency_key)
        return 201, {"request_id": "RBK-88231", "status": "PENDING_CONFIRMATION", "expires_at": "2026-09-15T11:12:00Z"}

    def create_human_case(self, reason: str, evidence: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        return 201, {"case_id": "HC-4471", "queue": "DISRUPTION_L2", "sla_minutes": 45, "reason": reason}
