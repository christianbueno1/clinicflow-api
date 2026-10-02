# ClinicFlow — Especificaciones técnicas

> Estado: **v0.1** (2026-10-01). Decisiones aprobadas; lo no cubierto aquí se considera "Por confirmar" y debe consultarse antes de implementar.
>
> Documentos relacionados: `MISSION.md`, `PRD.md`, `TECH-STACK.md`, `CHANGELOG.md`.

## 1. Arquitectura

Capas simples, en este orden de dependencia (una capa solo conoce a la inferior):

```text
routers (endpoints HTTP)
   ↓
services (reglas de aplicación)
   ↓
models / database (SQLAlchemy, sesión async)
```

- Los **routers** validan la entrada con esquemas Pydantic, llaman a un servicio y devuelven la respuesta. No contienen SQL ni reglas de negocio.
- Los **services** contienen la lógica de aplicación (búsqueda, creación, actualización, borrado lógico) y trabajan con la sesión async inyectada.
- Los **models** (SQLAlchemy) viven en `src/clinicflow_api/models/` y los **schemas** (Pydantic) en `src/clinicflow_api/schemas/`. Nunca se exponen modelos ORM directamente en las respuestas.
- Inyección de dependencias con `Depends` de FastAPI: `get_session()` para la sesión async y `get_settings()` (con `lru_cache`) para la configuración.

Estructura de paquetes:

```text
src/clinicflow_api/
├── main.py          # app FastAPI, lifespan, health checks
├── config.py        # Settings (pydantic-settings)
├── database.py      # engine, async_sessionmaker, get_session
├── models/          # modelos SQLAlchemy (Base, Patient)
├── schemas/         # esquemas Pydantic de entrada/salida
├── routers/         # endpoints por recurso (patients)
└── services/        # lógica de aplicación
```

## 2. Configuración

- Variables de entorno leídas por `Settings` (`pydantic-settings`): `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_NAME`, `DEBUG`, `API_BASE_URL`.
- La URL se construye como `postgresql+psycopg://...` (driver `psycopg` 3).
- `.env.example` y `.env.db.example` versionados; `.env` y `.env.db` locales e ignorados por git.
- Base de datos local: PostgreSQL 18.6 en Podman, gestionada con `scripts/podman/setup-db.sh` / `teardown-db.sh`.

## 3. Modelo de datos — `Patient`

Tabla `patients`:

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | UUID | PK, default `uuid4` |
| `first_name` | String(100) | NOT NULL, se normaliza con `strip()` |
| `last_name` | String(100) | NOT NULL, `strip()` |
| `date_of_birth` | Date | NOT NULL, no futura (validación Pydantic) |
| `sex` | String(1) / StrEnum | NOT NULL, valores `"M"` / `"F"`, constraint `ck_patients_sex` |
| `phone` | String(30) | NOT NULL, `strip()` |
| `identification_number` | String(10) | NOT NULL, UNIQUE, 10 dígitos (`^\d{10}$`, sin dígito verificador), `strip()` |
| `email` | String(254) | UNIQUE, nullable, `strip().lower()`; cadena vacía `""` se convierte en `None` |
| `address` | Text | nullable |
| `created_at` | DateTime(tz) | server_default `now()` |
| `updated_at` | DateTime(tz) | server_default `now()`, `onupdate=now()` |
| `deleted_at` | DateTime(tz) | nullable, NULL = activo |

Notas:

- La unicidad de `identification_number` y `email` la garantiza la base de datos (restricción UNIQUE) y es **global**: se aplica también frente a pacientes con borrado lógico (un paciente eliminado sigue bloqueando el valor). Los duplicados se traducen a **409**.
- `sex` se agrega al modelo (no existía) y es obligatorio en la creación; se modela como `StrEnum` con `Enum(native_enum=False, create_constraint=True)` para evitar el ENUM nativo de PostgreSQL.
- El borrado es lógico: `DELETE` fija `deleted_at = now()`. Todas las consultas de listado/detalle filtran `deleted_at IS NULL`; no hay forma de incluir eliminados por ahora.
- `Base` define `naming_convention` para constraints. El mapper usa `eager_defaults` para que `updated_at`/valores por defecto estén disponibles tras UPDATE en async.

## 4. Esquemas Pydantic (`schemas/`)

- `PatientCreate`: todos los campos obligatorios de creación (`first_name`, `last_name`, `date_of_birth`, `sex`, `phone`, `identification_number`); `email` y `address` opcionales. Validaciones: cédula con patrón `^\d{10}$`, `sex` enum M/F, `date_of_birth` no futura, normalización de `email` (`""` → `None`) y cédula.
- `PatientUpdate`: todos opcionales. `email`/`address` aceptan `null` para limpiarlos. `identification_number` es de solo lectura (no se puede modificar vía PATCH). Solo se aplican los campos enviados.
- `PatientResponse`: representación completa devuelta por la API (incluye `id`, timestamps; excluye `deleted_at`).
- `PatientListResponse`: `{ "items": [PatientResponse], "total": int, "limit": int, "offset": int }`.

## 5. API — endpoints

Prefijo: `/api/v1`.

| Método | Ruta | Descripción | Éxitos | Errores |
|---|---|---|---|---|
| POST | `/api/v1/patients` | Crear paciente | 201 | 409, 422 |
| GET | `/api/v1/patients` | Listar (paginado + filtros) | 200 | 422 |
| GET | `/api/v1/patients/{id}` | Detalle | 200 | 404 |
| PATCH | `/api/v1/patients/{id}` | Actualización parcial | 200 | 404, 409, 422 |
| DELETE | `/api/v1/patients/{id}` | Borrado lógico | 204 | 404 |
| GET | `/health` | Liveness | 200 | — |
| GET | `/health/db` | Conectividad con la BD | 200 | 500 |

### Listado — paginación y filtros

- Paginación: `limit` (default 20, máximo 100) y `offset` (default 0). La respuesta incluye `total`, `limit`, `offset`.
- Filtros (todos opcionales, combinables con AND):
  - `name`: contiene (case-insensitive) en `first_name` o `last_name`.
  - `email`: contiene (case-insensitive).
  - `identification_number`: contiene (case-insensitive).
  - `phone`: contiene (case-insensitive).
  - `sex`: exacto, `"M"` o `"F"`.
  - `age`: edad exacta en años cumplidos a hoy, derivada de `date_of_birth`.
- Orden por defecto: `created_at` descendente (más recientes primero).

### Errores

Formato uniforme: `{ "detail": "mensaje" }`. Los errores de validación de FastAPI (422) usan su estructura por defecto (`{ "detail": [ {loc, msg, type}, ... ] }`).

- 404: recurso inexistente o eliminado lógicamente.
- 409: conflicto de unicidad (`identification_number` o `email` duplicados).
- 422: entrada inválida.

## 6. Migraciones

- Alembic con plantilla **async**, carpeta `alembic/` en la raíz del repo.
- Migraciones generadas con `alembic revision --autogenerate -m "<mensaje>"` y revisadas a mano antes de aplicar.
- Aplicar con `alembic upgrade head` contra la BD de Podman.

## 7. Pruebas

- Runner: `pytest` + `pytest-asyncio`, modo `asyncio_mode = "auto"`.
- Carpeta `tests/` en la raíz con estructura espejo de `src/` (p. ej. `tests/test_patients.py`).
- Pruebas de integración contra la base de datos real de Podman (BD de prueba separada), no mocks de la capa de datos.
- Cobertura objetivo: 80% (según PRD).
- Calidad: `ruff` (lint + format) y `mypy` para verificación de tipos.

## 8. Convenciones

- Código, tablas, columnas y rutas en **inglés**; documentación en español.
- Estructura por capas: `routers/`, `services/`, `models/`, `schemas/` bajo `src/clinicflow_api/`. (La decisión previa de estructura plana del 2026-09-30 quedó reemplazada el 2026-10-01.)
- Rutas en plural (`/patients`), código Python en `snake_case`.
- Timestamps con zona horaria (`DateTime(timezone=True)`); normalización de texto en el modelo y en los esquemas (ver §3).
- El `commit` de la sesión se hace en la capa de **servicio**, no en el router ni en la dependencia de sesión.
- Alembic: la URL de la BD se fija en `env.py` desde `Settings` (nunca con contraseña en `alembic.ini` versionado).

