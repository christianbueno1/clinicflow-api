# ClinicFlow — Sprint Backlog

> Fase activa: **5 — Modelo SQLAlchemy de Paciente** (2026-10-01).
> Solo se detallan las tareas de esta fase. Al terminar, actualizar `ROADMAP.md`, `PRODUCT_BACKLOG.md` y `CHANGELOG.md` y cerrar la fase.

Leyenda de estado: **Pendiente** · **En curso** · **Hecho**.

| # | Tarea | Hecho cuando | Estado |
|---|---|---|---|
| 5.1 | `naming_convention` en `Base` (models/base.py) | Los constraints (unique, fk, ck, pk, ix) tienen nombres deterministas; p. ej. `ck_patients_sex` | Hecho |
| 5.2 | Campo `sex` como `StrEnum` con `Enum(native_enum=False, create_constraint=True)` | La columna valida M/F y el constraint queda como `ck_patients_sex` | Pendiente |
| 5.3 | Cédula: `identification_number` como `String(10)` y ajuste del validador (strip; sin `.upper()`) | El modelo y el validador reflejan 10 dígitos | Pendiente |
| 5.4 | `email`: cadena vacía `""` se convierte en `None` en el `@validates` | `""` ya no se persiste como cadena | Pendiente |
| 5.5 | `eager_defaults` en el mapper de `Patient` | `updated_at`/valores por defecto legibles tras UPDATE en async sin `MissingGreenlet` | Pendiente |
| 5.6 | Verificación del modelo: metadata SQLAlchemy, 11+1 columnas, tipos y nulabilidad, constraints únicos y de check | Script/REPL imprime la metadata correcta | Pendiente |
| 5.7 | Calidad: `ruff check` y `ruff format` en verde | Sin errores ni formato pendiente | Pendiente |
