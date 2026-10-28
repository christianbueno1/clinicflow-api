# ClinicFlow — Changelog y registro de decisiones

> Historia relevante del proyecto: cambios significativos y decisiones con su fecha y motivo.
> Para el estado técnico vigente, ver `SPECIFICATIONS.md` y `TECH-STACK.md`.

## 2026-10-01

### Documentación

- `TECH-STACK.md` pasa a v0.2 y se convierte en fuente única del stack (se elimina `specs/tech-stack.md`).
- Nuevo `SPECIFICATIONS.md` v0.1 con arquitectura, modelo, esquemas, endpoints, errores, migraciones, pruebas y convenciones.
- La tabla de decisiones del `PRD.md` se traslada aquí; el PRD queda solo con alcance y requisitos.
- Se eliminan `specs/mission.md` y `specs/roadmap.md`; el roadmap vive en `ROADMAP.md` (raíz).
- Se eliminan los borradores en `docs/` (`roadmap-update-2026-09-30.md`, `clinicflow-roadmap-update-task5.md`, `draf-notes.md`): su contenido vigente ya está incorporado en `ROADMAP.md`/`CHANGELOG.md`/`SPECIFICATIONS.md`/`README.md`.
- Convenciones en `SPECIFICATIONS.md` §8 y decisiones en este CHANGELOG: reemplaza la propuesta de `docs/conventions.md` + `docs/decisions.md`.

### Decisiones

| Tema | Decisión | Motivo |
|---|---|---|
| Python | 3.14 fijado con uv | Ya declarado en `.python-version` y `requires-python` |
| PostgreSQL | 18.6 (`postgres:18.6-trixie`) | Ya en uso en `.env.db` |
| SQLAlchemy | 2.1.x (`sqlalchemy[asyncio]`) | Ya en `pyproject.toml`; nota `greenlet` incluido vía extra |
| Driver | `psycopg` 3 | Ya en uso |
| Estructura | Por capas (`routers/`, `services/`, `models/`, `schemas/`) | Reemplaza la decisión de estructura plana del 2026-09-30 |
| Arquitectura | Capas simples router → servicio → acceso a datos; DI con `Depends` | Proporcional al objetivo de aprendizaje |
| Listado | `limit`/`offset` (default 20, máx. 100), `total`/`limit`/`offset` en respuesta | Decisión 2026-10-01 |
| Filtros | nombre, email, identification_number, phone (contiene, case-insensitive); sex y age exactos | Decisión 2026-10-01 |
| Orden | `created_at` descendente | Confirmado 2026-10-01 |
| Borrado | Lógico (`deleted_at`); excluido de listado/detalle; sin forma de incluirlos aún | Confirmado |
| Unicidad | Global de cédula y correo, también frente a borrados lógicos | Confirmado 2026-09-30 |
| Update | `PATCH` únicamente; `email`/`address` aceptan `null` para limpiar; `identification_number` solo lectura | Confirmado |
| Commit | En la capa de servicio | Confirmado |
| Cédula | 10 dígitos (`^\d{10}$`), validación solo en Pydantic, sin dígito verificador | Confirmado 2026-09-30 |
| `email` vacío | `""` se convierte en `None` | Evita choque de UNIQUE |
| `sex` | `StrEnum` male/female con `Enum(native_enum=False, create_constraint=True, length=6)`, obligatorio | Confirmado |
| `Base` | `naming_convention` en constraints (`ck_patients_sex`, etc.) | Confirmado |
| Sessions | `eager_defaults` en el mapper para evitar `MissingGreenlet` tras UPDATE | Confirmado |
| Alembic | URL en `env.py` desde `Settings`; nunca contraseña en `alembic.ini` | Seguridad |
| Errores | `{ "detail": "mensaje" }`; 201/200/204/404/409/422 | Confirmado |
| Pruebas | `pytest` + `pytest-asyncio`, integración contra BD real de Podman, cobertura 80% | Confirmado |
| Calidad | `ruff` (lint+format) y `mypy` | Confirmado |

## 2026-09-30

- Fases 1–4 completadas (proyecto base, configuración, Podman, conexión async).
- Fase 5 (modelo Patient) iniciada; atributos del modelo definidos en `src/clinicflow_api/models/patient.py`.
- Decisiones registradas en `docs/roadmap-update-2026-09-30.md` (borrado lógico, unicidad global, cédula ecuatoriana, campos obligatorios/opcionales, normalización, documentación por fase).

## 2026-09-29

- Borrador inicial de `specs/tech-stack.md` y `specs/roadmap.md`; verificación de versiones en web.
