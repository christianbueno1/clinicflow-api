# ClinicFlow API

API REST de práctica para aprender desarrollo backend (CRUD de pacientes). Ver `MISSION.md`, `PRD.md`, `TECH-STACK.md`, `SPECIFICATIONS.md`, `ROADMAP.md` y `CHANGELOG.md`.

## Comandos útiles

```bash
# Levantar la API en desarrollo
uv run fastapi dev src/clinicflow_api/main.py

# Listar las bases de datos de la BD local en Podman
podman exec clinicflow-db-box psql -U krs -d clinicflow_db -x -c "\l"

# Base de datos local
scripts/podman/setup-db.sh
scripts/podman/teardown-db.sh
```
