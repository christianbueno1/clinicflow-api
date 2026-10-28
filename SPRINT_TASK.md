# ClinicFlow — Sprint Task

> Tarea activa única. Al finalizar, marcarla Hecho en `SPRINT_BACKLOG.md`, hacer commit atómico y cargar la siguiente.

## Tarea actual: 5.5 — `eager_defaults` en el mapper de `Patient`

**Origen:** fase 5 · HU-04 (`PRODUCT_BACKLOG.md`) · `SPECIFICATIONS.md` §3.

**Qué hacer:**

1. `eager_defaults` en el mapper de `Patient`.

**Criterio de hecho:**

- `updated_at`/valores por defecto legibles tras UPDATE en async sin `MissingGreenlet`.

**Notas:**

- No hay migración aún (fase 6); el cambio afecta a la metadata del modelo.
