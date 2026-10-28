# ClinicFlow — Sprint Task

> Tarea activa única. Al finalizar, marcarla Hecho en `SPRINT_BACKLOG.md`, hacer commit atómico y cargar la siguiente.

## Tarea actual: 6.1 — Alembic: agregar `alembic` a dependencias y crear plantilla async + primera migración

**Origen:** fase 6 · HU-05 (`PRODUCT_BACKLOG.md`) · `SPECIFICATIONS.md` §6.

**Qué hacer:**

1. Agregar `alembic` a dependencias.
2. Crear plantilla async en `alembic/`.
3. Generar la primera migración (tabla `patients`).

**Criterio de hecho:**

- `alembic upgrade head` crea la tabla y `downgrade` la elimina.

**Notas:**

- URL de BD en `env.py` desde `Settings`.
