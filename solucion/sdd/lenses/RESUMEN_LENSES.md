# Resumen de Development Lenses — Disruption Companion V0

**Pasos SDD**: A4 (Lentes de Diseño) y A8 (Lentes de Implementación)  
**Modo**: Pragmático / Cumplimiento  
**Alcance analizado**: 15 specs funcionales de `sdd/specs/functional/` (V0)

---

## 1. Lentes de Diseño (Paso A4)

| Dimensión | Sublentes relevantes | Aplicación en V0 | Evidencia / Decisión |
|-----------|----------------------|------------------|----------------------|
| **A — Producto y Valor** | A01–A08 | Aplica | Foco en reducir incertidumbre del pasajero y contactos evitables al call center (`SRC-01-11`), resolviendo el caso base `ABC123` y sus variantes sin afirmar hechos no verificados. |
| **B — UX** | B01–B09 | Aplica (Visor mínimo) | Visor React sencillo con CSS propio alineado con `sdd/reports/DESIGN_CONTRACT.md` (sin HTML desnudo), mostrando contexto, alertas, reglas evaluadas, opción recomendada y botón de acción. |
| **C — Arquitectura** | C01–C11 | Aplica | Arquitectura Hexagonal (Puertos y Adaptadores) con modelo de dominio rico (DDD táctico). Dominio puro en Python 3.13 sin dependencias de FastAPI ni I/O; cadena secuencial `contexto → eventos → política → opciones`. |
| **D — Seguridad** | D01–D08, D10 | Aplica | Minimización de PII en todas las fronteras (`holder_first_name` como única excepción en vista; contexto reducido hacia `get_eligible_options`; cero PII en evidencia de casos humanos y en registros). Evaluador de reglas sin `eval`/`exec`. Dependencias fijadas a versiones estables (> 7 días de antigüedad). |
| **E — Código y Diseño** | E04, E05 | Aplica | Inversión de dependencias mediante protocolos/puertos en `backend/app/domain/ports.py` e inyección por constructor en `DisruptionCompanionService`. |
| **F — Datos como Producto** | F01, F02, F04, F05 | Aplica | Contratos explícitos tipados (`{campo: tipo}`), marcas de tiempo UTC ISO-8601 y trazabilidad de cada variable derivada con origen y supuestos (`A1`, `A2`, `A3`). |
| **G — IA** | G01–G08 | Aplica (Decisión de no usar IA en runtime) | V0 es 100 % determinístico en runtime (`SRC-05-01`): evita alucinaciones sobre políticas/costos, latencia adicional y exposición de PII a LLMs. Se documenta la arquitectura híbrida para consultas ambiguas en el README de ingeniería. |
| **H — Operaciones / SRE** | H01, H03, H06 | Aplica | Manejo explícito de fallas upstream (`502` si cae contexto, degradación segura si caen eventos/política/opciones, reintentos con `idempotency_key` ante `503 UPSTREAM_TIMEOUT` indeterminado). |
| **I — Enterprise Readiness** | I01–I05, I07, I08 | Aplica | Trazabilidad completa por `decision_id`, salud del servicio (`/ping`) y configuración inyectable. |
| **J — Variabilidad** | J01–J05 | Aplica | Ejes de cambio aislados detrás de puertos: herramientas externas (`MockToolsAdapter` intercambiable por HTTP real), reglas de política versionadas y catálogo de escenarios. |
| **K — Ente Vivo** | K02, K03 | Aplica | Coherencia entre lenguaje ubicuo (`GLOSSARY.md`), contratos (`EXTERNAL_CONTRACTS.md`) y módulos de dominio. |
| **L — Machine Learning** | L01 | No aplica (verificable) | L01: El sistema V0 no entrena ni ejecuta modelos de ML; la evaluación de políticas es determinística por requisitos de exactitud y control de alto impacto (`SRC-05-01`). |

---

## 2. Lentes de Implementación (Paso A8 — Guardia por Ciclo TDD)

| Dimensión | Sublentes activos | Regla obligatoria en cada ciclo TDD |
|-----------|-------------------|-------------------------------------|
| **E — Código y Diseño** | E01–E03, E06–E13 | Funciones de **máximo 10 líneas** y **máximo 3 parámetros**; nombres expresivos en inglés; retornos tempranos; una sola responsabilidad por función; WTF Review de 3 pasadas (comprensión, necesidad, proporcionalidad) tras cada refactor. |
| **D — Seguridad** | D06 | Validación estricta de esquemas de entrada; parser de condiciones con lista blanca de tokens sin `eval`/`exec`; escape de texto plano en UI React; prohibición de PII en trazas y respuestas de error. |
| **F — Datos** | F03, F06 | Inmutabilidad de modelos de dominio y preservación de razones de descarte en eventos y opciones. |
| **L — ML** | L09–L36 | No aplica: L01 determinó ausencia de modelos ML en runtime. |
