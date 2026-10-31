# ClinicFlow API

API REST de práctica para aprender desarrollo backend (CRUD de pacientes). Ver `MISSION.md`, `PRD.md`, `TECH-STACK.md`, `SPECIFICATIONS.md`, `ROADMAP.md` y `CHANGELOG.md`.

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

4. Levantar la API en desarrollo:

   ```bash
   uv run fastapi dev src/clinicflow_api/main.py
   ```

   Documentación interactiva en `/docs`.

## Comandos útiles

```bash
# Listar las bases de datos de la BD local en Podman
podman exec clinicflow-db-box psql -U krs -d clinicflow_db -x -c "\l"
```
