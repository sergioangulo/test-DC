# Recomendaciones de MCPs — Disruption Companion (paso SDD A2b)

**Estado:** recomendaciones opcionales y **no bloqueantes**. No se modificó ningún archivo de configuración de MCPs (`.mcp.json`): agregar un MCP requiere la confirmación expresa del usuario (ver «Decisión»).
**Alcance del inventario:** los MCPs realmente disponibles en esta sesión de trabajo. La herramienta de descubrimiento automático de MCPs **no está disponible** en el servidor SDD de esta sesión; por eso el inventario es manual y se declara incompleto.

## 1. Inventario y clasificación por fase

| MCP / herramienta | Fase SDD | ¿Resuelve una necesidad real? | Recomendación | Razón verificable |
|---|---|---|---|---|
| `sdd-workflow` (ya conectado) | todas | Sí: pasos, plantillas de spec/RFC, lentes, revisión adversarial | **Mantener** (ya en uso) | Es el flujo pedido por el usuario |
| `claude-in-chrome` (extensión de navegador) | diseño | Parcial: leer la página de referencia de look & feel | **No adoptar para implementación/verificación** | El navegador de la extensión es remoto y **no alcanza `localhost`** (comprobado en la sesión de análisis): no sirve para ver el front ni para pruebas; además cada uso exige confirmación en pantalla |
| `claude.ai Claude Docs` (documentos en la nube) | documentación | No | **No usar** | El enunciado está marcado «Uso interno» (REQ-N-10, NFR-010): el entregable es un repositorio local con Markdown (DEC-03); publicar fuera exige autorización expresa |
| Artefactos publicados (Artifact) | documentación | No | **No usar** | Misma razón de confidencialidad: no se publica nada sin autorización |

## 2. Herramientas externas que no son MCP (para transparencia, DEC-37)

| Herramienta | Uso | Observación |
|---|---|---|
| Codex CLI (`codex exec`, solo lectura) | Auditoría externa en cada etapa, pedida por el usuario | Envía contenido derivado del enunciado a un servicio externo: queda anotado en la bitácora de IA (DOC-006). Su cupo se agotó durante A1/A2; las vueltas pendientes se reintentan |

## 3. Necesidades del proyecto sin MCP disponible

| Necesidad | Alternativa manual (fallback) |
|---|---|
| Captura visual del front (DESIGN_CONTRACT) | Wireframes ASCII ya incluidos; la captura con un navegador local (Playwright) queda **diferida y sujeta a autorización del usuario** (descarga de un navegador) |
| Escaneo de vulnerabilidades en dependencias | Revisión manual del lente D + `pip`/`npm audit` locales si el usuario lo autoriza |
| Revisión de PRs | No aplica: no hay remoto ni PRs |

## 4. Decisión (pendiente de confirmación del usuario)

- **MCPs a agregar a `.mcp.json`: ninguno.** Con el inventario disponible no hay un MCP que resuelva una necesidad real del proyecto distinto de los ya conectados.
- El usuario puede pedir lo contrario; la ausencia de MCPs adicionales **no bloquea** el flujo.
- Referencia cruzada: el paso A4 (lente I, Enterprise Readiness) debe citar este documento.
