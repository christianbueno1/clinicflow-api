# ClinicFlow — Sprint Task

> Tarea activa única. Al finalizar, marcarla Hecho en `SPRINT_BACKLOG.md`, hacer commit atómico y cargar la siguiente.

## Tarea actual: 5.4 — `email`: cadena vacía `""` se convierte en `None` en la `@validates`

**Origen:** fase 5 · HU-04 (`PRODUCT_BACKLOG.md`) · `SPECIFICATIONS.md` §3.

**Qué hacer:**

1. `email`: cadena vacía `""` se convierte en `None` en la `@validates`.

**Criterio de hecho:**

- `""` ya no se persiste como cadena.

**Notas:**

- No hay migración aún (fase 6); el cambio afecta a la metadata del modelo y al validador.
