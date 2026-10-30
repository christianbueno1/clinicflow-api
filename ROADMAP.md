# ClinicFlow — Roadmap

> Estado: **v0.2** (2026-10-01). Orden de implementación a alto nivel, en fases de **1–2 horas**.
> Los detalles de cada fase se definen al empezarla. Antes de empezar una fase que toque un framework,
> se revisan sus novedades (ver `TECH-STACK.md`, sección 7).

## Estado actual

| Bloque | Estado |
|---|---|
| A — Cimientos (fases 1–4) | Completado |
| 5 — Modelo de Paciente | En curso |
| 6 en adelante | Sin empezar |

## Bloque A — Cimientos

| # | Fase | Hecho cuando | Estado |
|---|---|---|---|
| 1 | Proyecto base: `uv init`, estructura de carpetas, `.gitignore`, `.env.example`, endpoint `/health` | `uv run fastapi dev` responde en `/health` y `/docs` | Hecho |
| 2 | Configuración: lectura tipada de variables desde `.env` | La app falla con mensaje claro si falta una variable requerida | Hecho |
| 3 | Base de datos en Podman: scripts `setup` y `teardown` con variables | `setup` deja PostgreSQL accesible; `teardown` lo limpia; ambos son repetibles | Hecho |
| 4 | Conexión async: engine, sesión y dependencia de sesión | Un endpoint de prueba consulta la base y responde | Hecho |

## Bloque B — Primera entidad: Paciente, de punta a punta

| # | Fase | Hecho cuando | Estado |
|---|---|---|---|
| 5 | Modelo SQLAlchemy de Paciente: `naming_convention` en `Base`, campo `sex` (StrEnum valores male/female), cédula `String(10)`, validadores y `eager_defaults` | El modelo existe, compila contra la BD y las convenciones quedan documentadas | Hecho |
| 6 | Alembic (plantilla async) y primera migración; URL en `env.py` desde `Settings`; agregar `alembic` a dependencias | `upgrade` crea la tabla y `downgrade` la elimina | Hecho |
| 7 | Esquemas Pydantic (crear, actualizar, leer) con validaciones: cédula `^\d{10}$`, `sex` male/female, fecha no futura, `email ""` → `None`, normalización | Datos inválidos se rechazan con error 422 claro | Hecho |
| 8 | Capa de acceso a datos y servicio según la arquitectura elegida (capas simples): crear y obtener por id; `commit` en el servicio | Funciona sin pasar por HTTP | -- |
| 9 | Endpoints `POST` y `GET` por id bajo `/api/v1` | Se crea y consulta un paciente desde `/docs` | -- |
| 10 | Endpoints de listado (paginado con filtros), actualización (`PATCH`) y borrado (lógico) | CRUD completo funcionando desde `/docs` | -- |
| 11 | Manejo de errores consistente (404, 409, 422) y códigos de estado | Todos los errores comparten el mismo formato; el 409 cubre también choques con pacientes borrados | -- |
| 12 | Datos de ejemplo (personajes y casos de *Dr. House*) con script de carga; cédulas de 10 dígitos y sexo M/F | Un comando deja la base con datos simulados | -- |

## Bloque C — Calidad (se introduce ahora, no antes)

| # | Fase | Hecho cuando |
|---|---|---|
| 13 | Base de pruebas y pruebas unitarias (`pytest` + `pytest-asyncio`) | Las pruebas unitarias corren con un solo comando |
| 14 | Pruebas de integración contra una base de prueba en Podman | Cubren el CRUD completo de Paciente |
| 15 | Linter, formateo y verificación de tipos (`ruff`, `mypy`); hooks de git | El commit se bloquea si no pasan |
| 16 | CI | Cada push ejecuta pruebas y verificaciones |

## Bloque D — Ampliación (abierto, orden por decidir)

Candidatas, sin orden ni compromiso:

- Entidad **Médico**, repitiendo el patrón para validar que las convenciones funcionan.
- Entidad **Cita**, con relaciones entre entidades.
- Seguridad: autenticación, roles, límites de tasa.
- Observabilidad y rendimiento (tras la explicación pendiente).
- Despliegue y pruebas de carga.

## Cierre de cada fase

Cada fase actualiza `SPECIFICATIONS.md` (si cambia el diseño vigente) y/o `CHANGELOG.md` (decisiones tomadas), y deja verificado su criterio de "hecho".

## Pendientes que afectan al roadmap

- Visibilidad de pacientes con borrado lógico: excluidos por defecto (definido 2026-10-01; sin `include_deleted` por ahora).
- Herramientas concretas de CI y gestor de hooks: se deciden en la fase correspondiente (fases 15–16).
- Refactor de `database.py` a patrón factory (settings al llamar al engine/sesión): diferido hasta que Alembic o las pruebas lo necesiten.
