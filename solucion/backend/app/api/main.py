import os
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
from app.adapters.mock_tools import MockToolsAdapter
from app.application.companion_service import DisruptionCompanionService
from app.domain.ports import FixedClock, InMemoryDecisionStore

VIEWER_PATH = os.path.join(os.path.dirname(__file__), "viewer.html")

app = FastAPI(title="Disruption Companion V0 API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tools_adapter = MockToolsAdapter("BASE_TC01")
clock_adapter = FixedClock("2026-09-15T11:02:47Z")
decision_store = InMemoryDecisionStore()
companion_service = DisruptionCompanionService(tools_adapter, clock_adapter, decision_store)


class EvaluateRequest(BaseModel):
    caller: str = "user"


class AcceptRequest(BaseModel):
    decision_id: str


class ScenarioRequest(BaseModel):
    scenario_id: str


@app.get("/", response_class=HTMLResponse)
def viewer_page() -> str:
    with open(VIEWER_PATH, encoding="utf-8") as fh:
        return fh.read()


@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    return "pong"


@app.get("/api/dev/scenarios")
def list_scenarios() -> dict[str, Any]:
    meta = tools_adapter.current_scenario_meta()
    return {**meta, "scenarios": tools_adapter.list_scenarios()}


@app.put("/api/dev/scenario")
def activate_scenario(body: ScenarioRequest) -> Any:
    try:
        decision_store.decisions.clear()
        decision_store.operations.clear()
        decision_store.human_cases.clear()
        return tools_adapter.activate_scenario(body.scenario_id)
    except KeyError:
        return JSONResponse(status_code=404, content={"error": "SCENARIO_NOT_FOUND", "detail": "Escenario no encontrado."})


@app.post("/api/v1/trips/{booking_id}/evaluate")
def evaluate_trip(booking_id: str, body: EvaluateRequest) -> Any:
    if body.caller != "user":
        return JSONResponse(status_code=422, content={"error": "VALIDATION_ERROR", "detail": "Modo caller no soportado en V0."})
    try:
        return companion_service.evaluate_trip(booking_id)
    except KeyError:
        return JSONResponse(status_code=404, content={"error": "NOT_FOUND", "detail": "No encontramos el recurso solicitado."})


@app.post("/api/v1/trips/{booking_id}/options/{option_id}/accept")
def accept_option(booking_id: str, option_id: str, body: AcceptRequest) -> Any:
    try:
        return companion_service.accept_option(booking_id, option_id, body.decision_id)
    except KeyError:
        return JSONResponse(status_code=404, content={"error": "NOT_FOUND", "detail": "No encontramos el recurso solicitado."})
    except ValueError:
        return JSONResponse(status_code=422, content={"error": "OPTION_NOT_OFFERED", "detail": "La opción indicada no fue ofrecida."})
