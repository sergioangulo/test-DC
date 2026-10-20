import ast
import glob
import os
from fastapi.testclient import TestClient
from app.api.main import app


def test_ping_and_scenario_endpoints_and_base_flow():
    client = TestClient(app)
    ping_res = client.get("/ping")
    assert ping_res.status_code == 200
    assert ping_res.text == "pong"

    scen_res = client.get("/api/dev/scenarios")
    assert scen_res.status_code == 200
    assert len(scen_res.json()["scenarios"]) >= 5

    act_res = client.put("/api/dev/scenario", json={"scenario_id": "BASE_TC01"})
    assert act_res.status_code == 200

    eval_res = client.post("/api/v1/trips/ABC123/evaluate", json={"caller": "user"})
    assert eval_res.status_code == 200
    view = eval_res.json()
    assert view["decision_state"] == "PENDIENTE_APROBACION"
    assert view["proposed_option_id"] == "O1"
    raw_json = eval_res.text
    assert "Ana Prueba" not in raw_json
    assert "Lucas Prueba" not in raw_json

    acc_res = client.post(
        "/api/v1/trips/ABC123/options/O1/accept",
        json={"decision_id": view["decision_id"]},
    )
    assert acc_res.status_code == 200
    assert acc_res.json()["outcome"] == "HUMAN_CASE_CREATED"


def test_clean_code_ast_limits_and_domain_isolation():
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app"))
    py_files = glob.glob(os.path.join(app_dir, "**", "*.py"), recursive=True)
    violations: list[str] = []
    for path in py_files:
        rel = os.path.relpath(path, app_dir)
        tree = ast.parse(open(path, encoding="utf-8").read(), filename=rel)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                lines = (node.end_lineno or node.lineno) - node.lineno + 1
                params = [a.arg for a in node.args.args if a.arg not in ("self", "cls")]
                if lines > 10:
                    violations.append(f"{rel}:{node.name} has {lines} lines (>10)")
                if len(params) > 3:
                    violations.append(f"{rel}:{node.name} has {len(params)} params (>3)")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                violations.append(f"{rel} uses forbidden {node.func.id}")
    assert violations == []
