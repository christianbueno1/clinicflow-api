```bash
uv run fastapi dev src/clinicflow_api/main.py

podman exec clinicflow-db-box psql -U krs -d clinicflow_db -x -c "\l"

uv run ruff check
uv run ruff check src/clinicflow_api/models/base.py
# modificar el archivo y luego:
uv run ruff check --fix src/clinicflow_api/models/base.py

# modificar el archivo y luego:
uv run ruff format src/clinicflow_api/models/base.py

# sin modificar
uv run ruff format --check src/clinicflow_api/models/base.py
```