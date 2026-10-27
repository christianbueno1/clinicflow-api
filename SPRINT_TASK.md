# ClinicFlow — Sprint Task

> Tarea activa única. Al finalizar, marcarla Hecho en `SPRINT_BACKLOG.md`, hacer commit atómico y cargar la siguiente.

## Tarea actual: 5.3 — Cédula: `identification_number` como `String(10)` y ajuste del validador (strip; sin `.upper()`)

**Origen:** fase 5 · HU-04 (`PRODUCT_BACKLOG.md`) · `SPECIFICATIONS.md` §3.

**Qué hacer:**

1. `identification_number` como `String(10)`.
2. Ajustar el validador del modelo: `strip()`; sin `.upper()`.

**Criterio de hecho:**

- El modelo y el validador reflejan 10 dígitos.

**Notas:**

- La validación del patrón `^\d{10}$` sigue siendo responsabilidad de los esquemas Pydantic (fase 7).
- No hay migración aún (fase 6); el cambio afecta a la metadata del modelo y al validador.
