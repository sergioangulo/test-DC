# Backlog Consolidado — Disruption Companion (Paso A11)

| ID | Tipo | Origen | Descripción | Versión destino |
|----|------|--------|-------------|-----------------|
| **DEBT-V0-01** | Evolución (S-V0-1) | `02-sf-01-1`, `17-sf-02-1` | Validar cabecera de sesión y rate-limiting en aplicación cuando no opere detrás de un API Gateway. | `sdd/specs/V1` |
| **DEBT-V0-02** | Evolución (S-V0-2) | `04-sf-01-3` | Reordenamiento automático de segmentos desordenados y detección de cadenas rotas en lecturas upstream. | `sdd/specs/V1` |
| **DEBT-V0-03** | Evolución (S-V0-3) | `14-sf-01-13`, `36-f-04` | Persistencia relacional SQLite (`decisions`, `operations`, `human_cases`) y endpoint `GET /api/v1/decisions/{id}`. | `sdd/specs/V1` |
| **DEBT-V0-04** | Evolución (S-V0-4) | `19-sf-02-3`, `27-f-03` | Revalidación cuádruple de huella previa a escritura y diálogo separado de caso humano manual con 3 motivos. | `sdd/specs/V1` |
| **IDEA-V2-01** | Nueva capacidad | `51-f-08`, `64-f-11` | Modo proactivo `caller = "system"` con `X-Service-Key` e invocación de `notify_passenger` con enfriamiento de 24 h. | `sdd/specs/V2` |
| **IDEA-V2-02** | Operación CLI | `47-f-07`, `60-f-10` | Comandos CLI de purga de retención a 30 días (`purge`) y reporte de métricas (`metrics`). | `sdd/specs/V2` |
| **IDEA-V2-03** | UI Avanzada | `78`..`102` | Micro-interacciones de UI: cuenta regresiva en vivo, esqueleto de lentitud a 1,5 s, gestión de foco y tests de catálogo de textos. | `sdd/specs/V2` |
