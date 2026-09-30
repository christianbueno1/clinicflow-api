```bash
uv run fastapi dev src/clinicflow_api/main.py

podman exec clinicflow-db-box psql -U krs -d clinicflow_db -x -c "\l"
```