# Guía de revisión — qué cambió en los requerimientos (Etapa 0 → Implementación V0)

> **Estado actual (Cierre V0)**: A partir del universo completo de 104 specs (`sdd/specs/functional_all/`), el alcance se dividió en **`sdd/specs/V0/` (15 specs esenciales implementados en `sdd/specs/functional/` en Python 3.13)**, **`sdd/specs/V1/` (34 specs)** y **`sdd/specs/V2/` (55 specs)**. Además se incorporó **`FR-114`** (separación entre la Vista Limpia del Pasajero arriba y el Panel Gris de Soporte/Debug abajo) y se verificó que la aprobación humana por menor dependa estrictamente de la política activa (`R5`).
> Documento histórico revisado en Etapa 0: `docs/REQUERIMIENTOS_V1.md` (commit `0dd875c`). El primer borrador salió solo de tus decisiones; luego pasó por **3 vueltas de /codex, 1 del Step Reviewer y 3 del CTO interno** (≈ 40 defectos).
> Esta guía no repite el documento: lista **qué se añadió o cambió y por qué**, y **qué debes confirmar tú**.

## A. Lo que debes confirmar (decisiones que tomé yo o que interpreté)

| ID | Qué | Dónde | Por qué importa |
|---|---|---|---|
| **H-01** | Ninguna política externa entra al diseño, aunque DEC-05 figuraba como «incorpora info externa: Sí». Mandaron tus notas. | §1 | Si querías usar 31 min de la aerolínea en v1, cambia FR-005/FR-034 |
| **H-02** | DEC-09 marcaste «siempre humano», pero implementé **tus notas** (gana el más reciente no degradado; dos sanos contradictorios ⇒ soporte). | FR-010…014 | Es la regla central de eventos contradictorios |
| **H-03 / H-15** | El menor **no** es un disparador fijo de caso humano: lo decide `requires_human_approval` de la política (R5). Si la política no trae R5, **un menor podría rebookearse sin aprobación**. | FR-035, FR-052 | DEC-16 decía «con un menor siempre caso humano» |
| **H-04** | «Confirmación» (DEC-14) = **clic del pasajero**; «aprobación» = **agente**, solo si la política lo exige. | FR-050 | Son dos controles distintos |
| **H-06 / H-07** | DEC-10 y DEC-20 siguen **pendientes**; usé tus notas como supuesto provisional (`PROV`): sin umbral de antigüedad para eventos; `notify_passenger` no se invoca en v1. | FR-017, FR-085 | Confírmalas en el formulario |
| **H-08 / H-13** | MCT no provisto: conexión «desconocida» cuando el margen es < 45 min; **cambia el resultado esperado de TC-06** del análisis original. | FR-022, FR-023 | Evita un «sin conexión perdida» basado en un dato que falta |
| **H-09** | Todo retraso validado ≥ 1 min se informa; los derechos los fija la política. | FR-005 | DEC-05 pedía «umbral configurable por las políticas» |
| **H-10** | `booking_id` va en la auditoría (tu nota); truncado en logs; nunca nombre, edad ni RUT. | FR-090, FR-091 | |
| **H-14** | Dos desviaciones de la opción marcada: la llave idempotente **no** incluye la «decisión»; un tipo de pasajero distinto de `ADULT`/`CHILD` cuenta como menor **desconocido**. | FR-053, FR-024 | |
| **H-16** | El menú «Hablar con una persona» incluye «Tengo una consulta sobre compensaciones» (neutral, sin montos). FR-013 puede mandar a soporte la secuencia «a tiempo» → «retraso». | FR-060, FR-013 | Posible saturación de soporte |
| **S-09…S-19** | Constantes y supuestos míos: 45 min de incertidumbre de MCT, 60 s de reloj, 120 s de operación colgada, 1,5 s p95, 85 % de cobertura, SQLite local, retención de 30 días, prioridad de motivos (FR-063), etc. | §8b | Son valores propuestos, no dados |

## B. Lo que se añadió o cambió (por tema)

| Tema | Cambio | Origen |
|---|---|---|
| **Eventos** | Orden fijo de resolución: excluir degradados → buscar conflicto → gana el más reciente **entre afirmaciones no neutras** (`STATUS: SCHEDULED` nunca borra un retraso). Marcas de tiempo futuras y retrasos incoherentes se descartan. | Codex, Step Reviewer |
| **Anomalías** | Una anomalía en **cualquier** segmento bloquea la ejecución automática (decisión **BLOQUEADA**, FR-038). Más de un segmento retrasado ⇒ humano (FR-019). | Codex |
| **Derivaciones** | Fecha de llegada (+1 día), conexión sobre el último segmento, indicador `mct_provided`, supuestos A1/A2/A3 visibles, pernocte definido. | Codex, CTO |
| **Motor de reglas** | Gramática cerrada (`EQ` ≡ `==`, precedencia, tipos, límites); error de expresión ≠ valor desconocido (lógica de Kleene). | CTO |
| **Opciones** | Viable solo si hay derecho que la respalde y es coherente con el itinerario (origen, destino, salida); se registran **todas** las razones de descarte; reembolso con redacción **no afirmativa**. | CTO |
| **Escrituras** | Llave HMAC estable; registro de operaciones con ciclo de vida (`EN_CURSO`, `CREADA`, `INDETERMINADA`, `FALLIDA`, `EXPIRADA`); concurrencia; el cliente nunca aporta el contenido de la opción; se envían reserva y pasajeros (extensión DEC-18). | Codex, CTO |
| **Revalidación** | Huella de decisión (sin marcas de tiempo ni vigencia); relee también el **contexto del viaje**; no aplica a casos humanos. | Codex |
| **Casos humanos** | Motivo de enumeración cerrada (sin texto libre); 13 motivos con prioridad explícita; timeout ⇒ «indeterminado», sin reenvío automático. | Codex, Step Reviewer, CTO |
| **Seguridad** | Reserva ajena = inexistente (`404` idéntico); `decision_id` UUID; cabecera de sesión simulada apagada por defecto; lista blanca y lista negra de campos (§3.11); fixtures con datos ficticios. | Codex, CTO |
| **Pruebas** | De 20 a **41 TC**: se añadieron bordes de TTL, ciclo de vida, integridad, parser, concurrencia, autorización, evento degradado más reciente… | Step Reviewer, CTO |
| **Documentación** | DOC-011 (preguntas para Producto/Legal), DOC-012 (aprobación humana), DOC-013 (extensiones de contrato). | Step Reviewer |

## C. Cómo revisarlo rápido (≈ 20 min)

1. Lee **§1 (Hallazgos)** y la tabla de la sección A de esta guía: ahí están tus decisiones.
2. Lee **§2 (flujo)** y **FR-035, 038, 050, 052**: el control de acciones.
3. Revisa **§6 (pruebas)**: si un caso no refleja lo que esperas, es una regla mal entendida.
4. Anota en el chat los H/S que no apruebes; los cambio antes de pasar a la etapa de especificaciones.
