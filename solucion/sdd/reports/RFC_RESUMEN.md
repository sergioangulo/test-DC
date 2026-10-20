# Disruption Companion V0 — Resumen Ejecutivo (`RFC_RESUMEN`)

> Documento ejecutivo de 2 páginas para stakeholders de Producto, Operaciones e Ingeniería.  
> Para el detalle completo de las 4+1 vistas y los 15 procesos BPM, ver `sdd/reports/RFC_FINAL.md`.

---

## 1. ¿Qué es Disruption Companion V0 y qué problema resuelve?

**Disruption Companion V0** es un servicio de decisión para asistir a pasajeros cuyo vuelo sufrió una alteración operacional, combinando el contexto de su reserva, los eventos operacionales en tiempo real, las políticas vigentes de la aerolínea y las opciones de vuelos alternativos para ofrecer una explicación confiable y ejecutar el siguiente paso controlado.

- **Antes**: el pasajero recibía datos fragmentados o contradictorios entre fuentes, no sabía si perdería su conexión y debía llamar al call center incluso para cambios simples, mientras que automatizar a ciegas podía separar a un menor de su familia o infringir una política tarifaria.
- **Después**: el sistema filtra fuentes degradadas, calcula el impacto real en la conexión, evalúa las reglas versionadas de política sin intervención de modelos opacos, permite el cambio automático con un clic cuando es 100 % seguro y deriva a un especialista con toda la evidencia lista cuando viaja un menor o existe incertidumbre.

---

## 2. Funcionalidades Principales Implementadas en V0

1. **Evaluación determinística del viaje (`F-01`)**: cruza reserva, eventos, políticas y opciones candidatas entregando qué ocurrió, qué reglas aplican y qué alternativa es viable sin exponer datos personales.
2. **Acción controlada con protección ante fallos (`F-02`)**: ejecuta `create_rebooking_request` con llave idempotente cuando la decisión es `AUTOMATICA` (reintentando de forma segura ante errores `503` indeterminados), o abre un caso prioritario `create_human_case` cuando requiere aprobación humana.
3. **Visor interactivo de escenarios (`F-06` + `FE-02`)**: interfaz web que permite alternar entre los 6 escenarios del caso técnico y verificar la respuesta exacta del backend.

---

## 3. Decisiones Clave de Diseño

| Decisión | Por qué | Beneficio |
|----------|---------|-----------|
| **100 % determinístico en ejecución (sin IA en runtime)** | Las reglas de elegibilidad y costos son contratos exactos que no admiten alucinaciones ni latencia extra. | Cero riesgo de prometer derechos inexistentes y costo de inferencia igual a cero. |
| **Exclusión de fuentes degradadas y precedencia UTC** | Un evento antiguo o de una fuente degradada (`MONITORING_FEED`) no debe ocultar un retraso real de 160 min. | Exactitud en el estado informado al pasajero y bloqueo seguro ante conflictos reales. |
| **Aprobación humana gobernada por la política (`requires_human_approval`) y ante `503` persistente** | La exigencia de validación por un agente proviene de las reglas de política que se activan (ej. `R5` si la política pide revisión cuando viaja un menor, o `R2`), no de una condición fija en código; si la política no lo pide, la decisión es `AUTOMATICA`. | Desacoplamiento total entre el motor de decisión y las reglas de negocio vigentes, más protección ante fallos `503`. |

---

## 4. Cómo se ve el producto en funcionamiento

![Caso Base ABC123 en Disruption Companion V0](../screenshots/result/01-base-tc01.png)

---

## 5. Calidad Alcanzada

| Métrica | Resultado Verificado |
|---------|----------------------|
| **Runtime** | Python `3.13.16` + FastAPI `0.115.0` |
| **Suite de pruebas (Unitarias + Integración + E2E)** | **17 / 17 tests pasando (100 %)** |
| **Cobertura de código** | **93 % total** (`>= 87 %` en todos los módulos de dominio) |
| **Reglas Clean Code verificadas por AST** | **100 % de funciones ≤ 10 líneas y ≤ 3 parámetros**, 0 llamadas a `eval`/`exec` |
