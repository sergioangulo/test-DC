# Registro de decisiones automáticas (modo auto, personalidad demanding, 4 agentes)

| # | Etapa | Decisión | Razón | Aprobó |
|---|---|---|---|---|
| 1 | Setup | Ruta A de SDD (proyecto sin specs) adaptada a construcción desde cero (A9 = construir, no migrar). | `determine_sdd_path` no ofrece ruta de proyecto nuevo sin RFC. | El usuario (modo auto) |
| 2 | A0 | Se omite el scaffold Docker de A0: el repositorio ya existe (`git init`) y se ejecuta con venv + npm. | A0 paso 2: si existe el proyecto se salta; NFR-009 exige correr sin Docker. | Orquestador |
| 3 | Setup | Los requisitos usan FR-/NFR-/DOC- (formato SDD) y trazan a REQ/DEC/SRC del análisis previo. | Regla mandatory FR-XXX. | Orquestador |
| 6 | A1 | Cadena de lecturas SECUENCIAL por indicación del usuario: contexto → eventos → (si hay evento relevante validado) política → opciones → vista. Se revierte la paralelización de política y opciones. | Instrucción directa del usuario. | Usuario |
| 7 | A1 | La 4.ª vuelta de /codex NO pudo ejecutarse: `codex exec` devolvió «usage limit» (reinicio 19:56 hora del CLI). A1 tuvo 3 vueltas de /codex completas; la revisión externa de cierre queda PENDIENTE y se reintentará cuando se reinicie el cupo. | Límite externo, no omisión voluntaria. | Orquestador (a informar al usuario) |
