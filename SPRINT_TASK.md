# ClinicFlow — Sprint Task

> Tarea activa única. Al finalizar, marcarla Hecho en `SPRINT_BACKLOG.md`, hacer commit atómico y cargar la siguiente.

## Tarea actual: 5.1 — `naming_convention` en `Base`

**Origen:** fase 5 · HU-04 (`PRODUCT_BACKLOG.md`) · `SPECIFICATIONS.md` §3.

**Qué hacer:**

1. Revisar la metadata actual: los constraints de `Patient` aparecen con nombre `None`.
2. En `src/clinicflow_api/models/base.py`, definir `naming_convention` en el mapper de `Base`
   (convención estándar de SQLAlchemy: `ix`, `uq`, `ck`, `fk`, `pk` con nombres deterministas, p. ej. `ck_%(table_name)s_%(constraint_name)s` o equivalente con columnas).
3. Verificar que los constraints existentes (`uq` de `identification_number` y `email`) reciban nombre generado.

**Criterio de hecho:**

- `ruff check` y `ruff format` en verde.
- Un script/REPL imprime los nombres generados de los constraints y coinciden con la convención.
- Commit atómico con Conventional Commits, p. ej. `feat(db): add constraint naming conventions`.

**Notas:**

- No modificar todavía `patient.py` (eso es 5.2+).
- No hay migración aún (fase 6); el cambio afecta a la metadata del modelo.
