# Disruption Companion — Vertical Slice V0

Solución completa del caso **«Disruption Companion»**: backend en **Python 3.13** (FastAPI + dominio puro), visor **React/TypeScript**, especificación exhaustiva con metodología **SDD-TDD** y documentación de ingeniería trazable.

## Documento principal — leer primero

> ### [`solucion/sdd/reports/RFC_FINAL.md`](solucion/sdd/reports/RFC_FINAL.md) — La solución completa descrita
>
> **Este es el documento central de la entrega.** Describe la solución completa de extremo a extremo: fusiona el RFC funcional y el técnico bajo el modelo **4+1 Vistas de Kruchten** — arquitectura, los 15 procesos BPM implementados, contratos de las tools externas, resolución paso a paso del caso base, evidencia E2E con screenshots y todas las decisiones de diseño.
>
> Si solo vas a leer un documento, que sea este.

## Entregables solicitados

| Entregable | Documento |
|---|---|
| **1. Vertical Slice + instrucciones** | [`solucion/README.md`](solucion/README.md) — alcance V0/V1/V2, ejecución y verificación |
| **2. README de Ingeniería** (≤ 2 págs.) | [`solucion/docs/README_INGENIERIA.md`](solucion/docs/README_INGENIERIA.md) — problema entendido, outcome, resolución del caso base |
| **3. AI Usage & Decision Note** (≤ 1 pág.) | [`solucion/docs/AI_USAGE_NOTE.md`](solucion/docs/AI_USAGE_NOTE.md) — herramientas de IA, workflow propio y decisiones humanas |

## Documentación complementaria

| Documento | Contenido |
|---|---|
| [`solucion/docs/RUNBOOK.md`](solucion/docs/RUNBOOK.md) | Runbook operativo: arranque, endpoints, escenarios de demo |
| [`solucion/docs/BITACORA_IA.md`](solucion/docs/BITACORA_IA.md) | Bitácora horaria del trabajo asistido por IA |
| [`solucion/docs/DECISIONES_DE_TRABAJO.md`](solucion/docs/DECISIONES_DE_TRABAJO.md) | Las 37 decisiones de diseño revisadas y aprobadas |
| [`solucion/sdd/reports/RFC_TECHNICAL.md`](solucion/sdd/reports/RFC_TECHNICAL.md) | RFC técnico (vistas 4+1, contratos, evidencia) |
| [`solucion/sdd/reports/RFC_RESUMEN.md`](solucion/sdd/reports/RFC_RESUMEN.md) | Resumen ejecutivo del RFC |
| [`solucion/sdd/reports/E2E_EVIDENCE.md`](solucion/sdd/reports/E2E_EVIDENCE.md) | Evidencia de los 6 escenarios E2E con screenshots |
| [`solucion/sdd/reports/ARCHITECTURE.md`](solucion/sdd/reports/ARCHITECTURE.md) | Arquitectura limpia propuesta y justificación |
| [`solucion/sdd/reports/DESIGN_CONTRACT.md`](solucion/sdd/reports/DESIGN_CONTRACT.md) | Contrato visual/UX del visor |
| [`solucion/sdd/reports/EXTERNAL_CONTRACTS.md`](solucion/sdd/reports/EXTERNAL_CONTRACTS.md) | Contratos de las 7 tools externas simuladas |
| [`solucion/sdd/reports/FR_COVERAGE.md`](solucion/sdd/reports/FR_COVERAGE.md) | Cobertura de requisitos funcionales |
| [`solucion/sdd/reports/BUILD_VERIFICATION.md`](solucion/sdd/reports/BUILD_VERIFICATION.md) | Verificación de build y suite de tests |

## Proceso de análisis (Evidencia Etapa 0)

Carpetas `01_` a `06_` en la raíz: extracción de los 78 enunciados fuente (`01_Fuente_y_Trazabilidad/`), análisis ESF (`02_`), requerimientos trazables (`03_`), análisis de los datos de ejemplo (`04_`), políticas externas rescatadas por separado (`05_`) y el formulario de decisiones (`06_Decisiones/FORMULARIO_DECISIONES.html`). Ver [`00_LEEME.md`](00_LEEME.md) para el orden de lectura.

## Estructura de la solución

```
solucion/
├── backend/            # Python 3.13 · FastAPI · dominio puro (sin dependencias externas)
│   ├── app/domain/     # EventResolver, VariableDeriver, RuleEngine, OptionFilter, MessageBuilder
│   ├── app/adapters/   # MockToolsAdapter — 6 escenarios con fuentes degradadas
│   ├── app/api/        # FastAPI + visor web integrado
│   └── tests/          # unitarias, integración, E2E, calidad AST (Clean Code)
├── frontend/           # React + TypeScript + Vite — visor de disrupciones
├── sdd/                # Specs SDD: 104 funcionales (V0: 15 / V1: 34 / V2: 55)
│   ├── specs/          # functional (V0 implementado), V1, V2, functional_all, technical
│   ├── reports/        # RFC_FINAL, RFC_TECHNICAL, arquitectura, evidencias
│   └── screenshots/    # Evidencia visual E2E
└── docs/               # Entregables 2 y 3, runbook, bitácora, decisiones
```

## Ejecución rápida

```bash
# Backend + visor integrado (http://127.0.0.1:8000)
cd solucion/backend
python -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000

# Tests (unitarios + integración + E2E + calidad AST)
cd solucion/backend
python -m pytest -v --cov=app

# Frontend standalone (http://localhost:5173)
cd solucion/frontend && npm install && npm run dev
```

Instrucciones completas en [`solucion/docs/RUNBOOK.md`](solucion/docs/RUNBOOK.md).
