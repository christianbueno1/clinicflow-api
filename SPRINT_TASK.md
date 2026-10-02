# ClinicFlow — Sprint Task

> Tarea activa única. Al finalizar, marcarla Hecho en `SPRINT_BACKLOG.md`, hacer commit atómico y cargar la siguiente.

## Tarea actual: 5.2 — Campo `sex` como `StrEnum`

**Origen:** fase 5 · HU-04 (`PRODUCT_BACKLOG.md`) · `SPECIFICATIONS.md` §3.

**Qué hacer:**

1. Crear `sex` en `Patient` como `StrEnum` con valores `"M"` y `"F"`.
2. Columna: `Enum(Sex, name="sex", native_enum=False, create_constraint=True, length=1)` (o equivalente que genere el CHECK).
3. Verificar que el constraint resultante se llame `ck_patients_sex` (según la `naming_convention` de 5.1).

**Criterio de hecho:**

- `ruff check` y `ruff format` en verde.
- Un script/REPL imprime la columna y el constraint `ck_patients_sex`.
- Commit atómico con Conventional Commits, p. ej. `feat(db): add sex enum to patient model`.

**Notas:**

- `sex` es obligatorio (NOT NULL) en creación.
- `Enum` de SQLAlchemy: revisar la firma vigente en SQLAlchemy 2.1 antes de escribirlo (regla de actualidad).
