from fastapi.testclient import TestClient
from app.api.main import app


def test_e2e_all_six_scenarios_full_lifecycle():
    client = TestClient(app)

    # 1. BASE_TC01: Caso Base del PDF (retraso 160m + menor + conexion perdida -> PENDIENTE_APROBACION + O1 -> caso humano)
    client.put("/api/dev/scenario", json={"scenario_id": "BASE_TC01"})
    r1 = client.post("/api/v1/trips/ABC123/evaluate", json={"caller": "user"}).json()
    assert r1["decision_state"] == "PENDIENTE_APROBACION"
    assert r1["proposed_option_id"] == "O1"
    assert [o["option_id"] for o in r1["discarded_options"]] == ["O2", "O3"]
    a1 = client.post("/api/v1/trips/ABC123/options/O1/accept", json={"decision_id": r1["decision_id"]}).json()
    assert a1["outcome"] == "HUMAN_CASE_CREATED"
    assert a1["human_case"]["case_id"] == "HC-4471"

    # 2. ADULTOS_AUTOMATICO_TC07: Dos adultos sin menor -> AUTOMATICA -> create_rebooking_request 201 y luegoEXISTING_REQUEST
    client.put("/api/dev/scenario", json={"scenario_id": "ADULTOS_AUTOMATICO_TC07"})
    r2 = client.post("/api/v1/trips/ABC123/evaluate", json={"caller": "user"}).json()
    assert r2["decision_state"] == "AUTOMATICA"
    a2 = client.post("/api/v1/trips/ABC123/options/O1/accept", json={"decision_id": r2["decision_id"]}).json()
    assert a2["outcome"] == "REBOOKING_CREATED"
    assert a2["operation"]["request_id"] == "RBK-88231"
    a2_dup = client.post("/api/v1/trips/ABC123/options/O1/accept", json={"decision_id": r2["decision_id"]}).json()
    assert a2_dup["outcome"] == "EXISTING_REQUEST"

    # 3. CONFLICTO_FUENTES_TC03: Empate de timestamp entre fuentes sanas -> BLOQUEADA (SOURCE_CONFLICT)
    client.put("/api/dev/scenario", json={"scenario_id": "CONFLICTO_FUENTES_TC03"})
    r3 = client.post("/api/v1/trips/ABC123/evaluate", json={"caller": "user"}).json()
    assert r3["decision_state"] == "BLOQUEADA"
    assert "SOURCE_CONFLICT" in r3["blocking_reasons"]
    assert r3["policy"] is None
    assert r3["options"] == []

    # 4. SOLO_DEGRADADO_TC02: Solo fuente degradada MONITORING_FEED -> NO_VERIFIED_INFO, sin alerta falsa de 'a tiempo'
    client.put("/api/dev/scenario", json={"scenario_id": "SOLO_DEGRADADO_TC02"})
    r4 = client.post("/api/v1/trips/ABC123/evaluate", json={"caller": "user"}).json()
    assert r4["decision_state"] is None
    assert r4["segments"][0]["state"] == "NO_VERIFIED_INFO"

    # 5. SIN_OPCION_VIABLE_TC09: Solo O2 con 1 asiento para 2 pasajeros -> BLOQUEADA (NO_OPTION_COVERS_GROUP)
    client.put("/api/dev/scenario", json={"scenario_id": "SIN_OPCION_VIABLE_TC09"})
    r5 = client.post("/api/v1/trips/ABC123/evaluate", json={"caller": "user"}).json()
    assert r5["decision_state"] == "BLOQUEADA"
    assert r5["options"] == []
    assert "INSUFFICIENT_SEATS" in r5["discarded_options"][0]["discard_reasons"]

    # 6. UPSTREAM_TIMEOUT_TC14: 503 indeterminado en rebooking -> 2 reintentos con misma llave y derivacion a caso humano
    client.put("/api/dev/scenario", json={"scenario_id": "UPSTREAM_TIMEOUT_TC14"})
    r6 = client.post("/api/v1/trips/ABC123/evaluate", json={"caller": "user"}).json()
    assert r6["decision_state"] == "AUTOMATICA"
    a6 = client.post("/api/v1/trips/ABC123/options/O1/accept", json={"decision_id": r6["decision_id"]}).json()
    assert a6["outcome"] == "HUMAN_CASE_CREATED"
    assert a6["retries"] == 2


def test_user_story_2_customer_view_vs_support_debug_panel_separation():
    client = TestClient(app)
    client.put("/api/dev/scenario", json={"scenario_id": "BASE_TC01"})
    view = client.post("/api/v1/trips/ABC123/evaluate", json={"caller": "user"}).json()

    texts = [m["text"] for m in view["messages"]]
    assert any(t.startswith("Te proponemos: Cambiar tu vuelo a LA2412") for t in texts)
    assert any("necesita la validación de uno de nuestros agentes." in t for t in texts)
    assert any("Si prefieres no viajar, un agente puede revisar contigo las alternativas." in t for t in texts)
    assert view["actions"][0]["label"] == "Aceptar opción y contactar a un agente de soporte"

    client.put("/api/dev/scenario", json={"scenario_id": "SIN_OPCION_VIABLE_TC09"})
    view_no_opt = client.post("/api/v1/trips/ABC123/evaluate", json={"caller": "user"}).json()
    assert view_no_opt["actions"][0]["label"] == "Contactar a un ejecutivo"

    html = client.get("/").text
    assert "Estado de tu viaje" in html
    assert "Tienes una sugerencia pendiente de aprobación" in html
    assert "Información Operacional, Soporte y Trazabilidad (Debug Interno)" in html

