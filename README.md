# ClinicFlow API

API REST de práctica para aprender desarrollo backend con **FastAPI**, **SQLAlchemy 2 (async)** y **PostgreSQL**. Gestiona especialidades, doctores, pacientes y citas médicas, con reglas de negocio reales (solapamientos, estados, soft delete).

Documentación del proyecto: `MISSION.md`, `PRD.md`, `TECH-STACK.md`, `SPECIFICATIONS.md`, `ROADMAP.md` y `CHANGELOG.md`.

## Stack

- Python 3.14 gestionado con **uv**
- FastAPI + Pydantic v2
- SQLAlchemy 2.0 async + psycopg 3
- PostgreSQL en **Podman**
- Alembic (migraciones), pytest + httpx (tests), ruff (lint y formato)

## Entorno

- Fedora 44 Workstation (Linux).
- Solo la base de datos corre en contenedor: **Podman** debe estar instalado.
- La app corre en el host con Python 3.14 gestionado por **uv**.

## Puesta en marcha

1. Instalar dependencias:

   ```bash
   uv sync
   ```

2. Crear los archivos de entorno a partir de los ejemplos:

   ```bash
   cp .env.example .env
   cp .env.db.example .env.db
   ```

   Ajusta usuario/contraseña si lo deseas (deben coincidir entre ambos archivos).

3. Levantar la base de datos en Podman:

   ```bash
   scripts/podman/setup-db.sh
   ```

   Para detener y eliminar el contenedor, pod y red (el volumen de datos se conserva):

   ```bash
   scripts/podman/teardown-db.sh
   ```

4. Aplicar las migraciones:

   ```bash
   uv run alembic upgrade head
   ```

5. (Opcional) Cargar datos de prueba (idempotente, puede ejecutarse varias veces):

   ```bash
   uv run python scripts/seed.py
   ```

6. Levantar la API en desarrollo:

   ```bash
   uv run fastapi dev src/clinicflow_api/main.py
   ```

   Documentación interactiva en `http://127.0.0.1:8000/docs`.

## Endpoints

| Recurso | Rutas |
|---|---|
| Salud | `GET /health`, `GET /health/db` |
| Especialidades | `POST/GET /specialties`, `GET/PATCH/DELETE /specialties/{id}` |
| Doctores | `POST/GET /doctors` (filtros `specialty_id`, `is_active`), `GET/PATCH/DELETE /doctors/{id}` |
| Pacientes | `POST/GET /patients` (búsqueda `q`), `GET/PATCH/DELETE /patients/{id}` |
| Citas | `POST/GET /appointments` (filtros `patient_id`, `doctor_id`, `status`, `date_from`, `date_to`), `GET/PATCH /appointments/{id}`, `PATCH /appointments/{id}/status` |

## Reglas de negocio

- Cédula ecuatoriana validada (Módulo 10) en doctores y pacientes.
- Doctores y pacientes usan **soft delete** (`deleted_at`).
- No se puede eliminar un doctor o paciente con citas programadas a futuro (409).
- No se puede eliminar una especialidad con doctores asociados (409).
- Una cita no puede solaparse con otra del mismo doctor ni del mismo paciente (409). Las citas consecutivas están permitidas.
- Las fechas de las citas requieren zona horaria y deben ser futuras.
- El doctor de una cita debe estar activo.
- Estados de cita: `scheduled → completed | cancelled | no_show`. Los estados finales no admiten cambios. Las citas no se eliminan, se cancelan.

## Arquitectura

Capas con dependencias en una sola dirección:

```
routers → services → repositories → models
              ↘ schemas (Pydantic, sin importar de models)
```

```
src/clinicflow_api/
├── config.py  database.py  main.py
├── enums.py  models.py  schemas.py
├── repositories.py  services.py  validators.py
└── routers/
alembic/      # migraciones
scripts/      # seed y scripts de Podman
tests/        # pytest
```

## Migraciones

```bash
uv run alembic revision --autogenerate -m "descripcion"   # generar (revisar el archivo)
uv run alembic upgrade head                               # aplicar
uv run alembic downgrade -1                               # revertir la última
uv run alembic check                                      # modelos vs. base de datos
```

## Tests

Los tests usan una base de datos aparte (`clinicflow_test`) para no tocar los datos de desarrollo.

1. Crear la base de test:

   ```bash
   podman exec clinicflow-db-box psql -U krs -d postgres -c "CREATE DATABASE clinicflow_test;"
   ```

2. Crear `.env.test` (ignorado por git) con la URL de esa base, que debe terminar en `_test`:

   ```
   TEST_DATABASE_URL=postgresql+psycopg://krs:PASSWORD@localhost:5432/clinicflow_test
   ```

3. Ejecutar:

   ```bash
   uv run pytest -v
   ```

## Calidad de código

```bash
uv run ruff check --fix . && uv run ruff format .
```

## Comandos útiles

```bash
# Listar las bases de datos de la BD local en Podman
podman exec clinicflow-db-box psql -U krs -d clinicflow_db -x -c "\l"
```

Referencia de la API para el frontend: docs/API_REFERENCE.md.