# Runbook Operativo (1 página) — Disruption Companion V0 (`DOC-010`)

## 1. Arquitectura en Ejecución y Puertos

- **Servicio**: Monolito ligero en **Python 3.13** (`FastAPI` + `Uvicorn`) con visor web integrado.
- **Puerto por defecto**: `127.0.0.1:8000` (sirve tanto la API REST `/api/v1/*` y `/api/dev/*` como el visor web en `/`).
- **Dependencias externas en V0**: simuladas en memoria mediante `MockToolsAdapter` (`backend/app/adapters/mock_tools.py`).

---

## 2. Arranque, Verificación de Salud y Pruebas

| Operación | Comando | Resultado esperado |
|-----------|---------|--------------------|
| **Healthcheck** | `curl -i http://127.0.0.1:8000/ping` | `HTTP/1.1 200 OK` con cuerpo `pong` |
| **Levantar servicio** | `cd solucion/backend && C:/Users/maste/anaconda3/envs/companion313/python.exe -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000` | Servidor activo en `< 2 s` |
| **Ejecutar suite completa** | `cd solucion/backend && C:/Users/maste/anaconda3/envs/companion313/python.exe -m pytest -v --cov=app` | `19 passed`, cobertura `>= 93 %`, 0 violaciones AST |

---

## 3. Diagnóstico y Manejo de Incidentes Operacionales

| Síntoma / Código | Causa probable | Acción de mitigación del sistema y del operador |
|------------------|----------------|-------------------------------------------------|
| **Decisión `BLOQUEADA` con `SOURCE_CONFLICT`** | Dos fuentes operacionales sanas reportaron estados incompatibles con el mismo timestamp `recorded_at`. | El sistema **no** automatiza ni consulta opciones; ofrece al pasajero el botón «Contactar a un ejecutivo». Verificar salud del feed en el Panel Gris de Debug. |
| **Respuesta `503 UPSTREAM_TIMEOUT` en rebooking** | El proveedor de cambios tardó más del umbral o devolvió `503` (resultado indeterminado). | El sistema reintenta automáticamente hasta 2 veces con la **misma `idempotency_key`** y, si persiste, abre el caso `HC-4471` (`UPSTREAM_INDETERMINATE`) para que un agente verifique si la reserva se creó antes de reintentar manualmente. |
| **Segmento en `NO_VERIFIED_INFO`** | Todos los eventos del tramo provienen de fuentes listadas en `_meta.sources_degraded` (ej. `MONITORING_FEED`). | El sistema descarta el evento degradado y muestra «Sin información verificada en este momento» sin afirmar que el vuelo está a tiempo. |
| **Opciones descartadas (`NO_OPTION_COVERS_GROUP`)** | Las opciones devueltas tienen menos asientos que `passenger_count` (ej. `O2` con 1 asiento para 2 pasajeros). | El sistema nunca divide al grupo familiar; descarta la opción registrando `INSUFFICIENT_SEATS` en el panel de soporte y habilita «Contactar a un ejecutivo». |
