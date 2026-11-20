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


## Alembic

```bash
uv run alembic revision --autogenerate -m "add patients table"
uv run alembic upgrade head

# Probar que es reversible
uv run alembic downgrade -1
uv run alembic upgrade head

# Comprobar que modelo y base coinciden
uv run alembic revision --autogenerate -m check
```

## Database

```bash
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c '\dt'
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c '\d patients'
# para imprimar en vertical
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -x -c 'select * from patients;'
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c 'select * from specialties order by name;'
# extrae los doctores que son de Urologia
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c "select d.first_name, d.last_name, s.name as specialty from doctors d join specialties s on s.id = d.specialty_id where s.name = 'Urologia';"
# busca en tabla doctors por specialty_id 5885e82c-a775-4af6-bcb8-166b6bdadf14 sin join
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c "select * from doctors where specialty_id = '5885e82c-a775-4af6-bcb8-166b6bdadf14';"

# revision de Alembic
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db \
  -c 'select * from alembic_version;'

# comparalo
uv run alembic current
# table
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db \
  -c 'select count(*) from patients;'

# Prueba de escritura
# insercion valida
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c \
"insert into patients (id, first_name, last_name, date_of_birth, sex, phone, identification_number)
 values (gen_random_uuid(), 'Test', 'Paciente', '1990-01-01', 'male', '0999999999', '0000000001')
 returning id, first_name, sex, created_at, updated_at, deleted_at;"

# restricciones
# Cédula duplicada, debe violar uq_patients_identification_number:
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c \
"insert into patients (id, first_name, last_name, date_of_birth, sex, phone, identification_number)
 values (gen_random_uuid(), 'Otro', 'Paciente', '1991-02-02', 'female', '0988888888', '0000000001');"

# Sexo inválido, debe violar ck_patients_sex:
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c \
"insert into patients (id, first_name, last_name, date_of_birth, sex, phone, identification_number)
 values (gen_random_uuid(), 'X', 'Y', '1991-02-02', 'other', '0977777777', '0000000002');"

# Campo obligatorio nulo, debe violar not null:
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c \
"insert into patients (id, first_name, last_name, date_of_birth, sex, identification_number)
 values (gen_random_uuid(), 'X', 'Y', '1991-02-02', 'male', '0000000003');"

# limpieza
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c \
"delete from patients where identification_number = '0000000001';"
```

## Prepara uso de CURL en fedora

```bash
sudo dnf install -y jq     # si no lo tienes

BASE=http://127.0.0.1:8000
post() { curl -s -X POST "$BASE$1" -H "Content-Type: application/json" -d "$2"; }
sid()  { curl -s "$BASE/specialties?limit=100" | jq -r --arg n "$1" '.[] | select(.name==$n) | .id'; }

# 1. Especialidades del Princeton-Plainsboro
for s in "Medicina Diagnóstica" "Oncología" "Endocrinología" "Neurología" "Cirugía"; do
  post /specialties "{\"name\":\"$s\"}" > /dev/null
done

DIAG=$(sid "Medicina Diagnóstica"); ONCO=$(sid "Oncología")
ENDO=$(sid "Endocrinología");       NEURO=$(sid "Neurología"); CIR=$(sid "Cirugía")
echo $DIAG $ONCO $ENDO $NEURO $CIR

# 2. El equipo
post /doctors "{\"first_name\":\"Gregory\",\"last_name\":\"House\",\"identification_number\":\"1712345675\",\"license_number\":\"PPTH-0001\",\"specialty_id\":\"$DIAG\"}" | jq
post /doctors "{\"first_name\":\"James\",\"last_name\":\"Wilson\",\"identification_number\":\"1801234566\",\"license_number\":\"PPTH-0002\",\"specialty_id\":\"$ONCO\"}" | jq
post /doctors "{\"first_name\":\"Lisa\",\"last_name\":\"Cuddy\",\"identification_number\":\"0102030400\",\"license_number\":\"PPTH-0003\",\"specialty_id\":\"$ENDO\"}" | jq
post /doctors "{\"first_name\":\"Eric\",\"last_name\":\"Foreman\",\"identification_number\":\"1309876546\",\"license_number\":\"PPTH-0004\",\"specialty_id\":\"$NEURO\"}" | jq
post /doctors "{\"first_name\":\"Robert\",\"last_name\":\"Chase\",\"identification_number\":\"0701234569\",\"license_number\":\"PPTH-0005\",\"specialty_id\":\"$CIR\"}" | jq

# 3. Casos de error (el “todo es lupus” de las validaciones)
# 422: cédula inválida
curl -i -X POST $BASE/doctors -H "Content-Type: application/json" \
  -d "{\"first_name\":\"Lawrence\",\"last_name\":\"Kutner\",\"identification_number\":\"1234567890\",\"license_number\":\"PPTH-0006\",\"specialty_id\":\"$DIAG\"}"

# 409: licencia repetida (House ya tiene PPTH-0001)
curl -i -X POST $BASE/doctors -H "Content-Type: application/json" \
  -d "{\"first_name\":\"Chris\",\"last_name\":\"Taub\",\"identification_number\":\"1104680135\",\"license_number\":\"PPTH-0001\",\"specialty_id\":\"$CIR\"}"

# 404: especialidad inexistente
curl -i -X POST $BASE/doctors -H "Content-Type: application/json" \
  -d '{"first_name":"Amber","last_name":"Volakis","identification_number":"1104680135","license_number":"PPTH-0007","specialty_id":"3fa85f64-5717-4562-b3fc-2c963f66afa6"}'

# 4. Consultas, PATCH y soft delete
# Lista y filtros
curl -s "$BASE/doctors" | jq '.[] | {nombre: (.first_name + " " + .last_name), especialidad: .specialty.name}'
curl -s "$BASE/doctors?specialty_id=$ONCO" | jq

# House se pone en licencia (PATCH parcial)
HOUSE=$(curl -s "$BASE/doctors" | jq -r '.[] | select(.last_name=="House") | .id')
curl -s -X PATCH $BASE/doctors/$HOUSE -H "Content-Type: application/json" -d '{"is_active": false}' | jq .is_active

curl -s "$BASE/doctors?is_active=false" | jq '.[].last_name'

# Wilson renuncia (soft delete) y desaparece
WILSON=$(curl -s "$BASE/doctors" | jq -r '.[] | select(.last_name=="Wilson") | .id')
curl -i -X DELETE $BASE/doctors/$WILSON     # 204
curl -i $BASE/doctors/$WILSON               # 404


# 5. Verificar el soft delete en la base
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db \
  -c "SELECT last_name, is_active, deleted_at FROM doctors ORDER BY last_name;"

```

## Pytest

```bash
uv add --dev pytest pytest-asyncio httpx
podman exec -it clinicflow-db-box psql -U krs -d postgres -c "CREATE DATABASE clinicflow_test;"
# En pyproject.toml:
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
##
# Estructura
tests/
├── conftest.py
├── test_catalog.py
└── test_appointments.py
#
touch tests/conftest.py
touch tests/test_catalog.py
touch tests/test_appointments.py

# exporta la variable en tu shell
export TEST_DATABASE_URL="postgresql+psycopg://krs:TU_PASSWORD@localhost:5432/clinicflow_test"

```

## Docs

```bash
uv run python -c "import json; from clinicflow_api.main import app; print(json.dumps(app.openapi(), indent=2, ensure_ascii=False))" > docs/openapi.json
```

## Seed

```bash
uv run python scripts/seed_bulk.py --doctors 60 --patients 120
uv run python scripts/seed_bulk.py --doctors 60 --patients 120   # repetir: no duplica

curl -s "$BASE/doctors?limit=100" | jq length
curl -s "$BASE/doctors?skip=50&limit=25" | jq length
curl -s "$BASE/doctors?is_active=false&limit=100" | jq length
```

## OpenAPI

```bash
# 1. El primer comando: Exportar el esquema OpenAPI a un archivo JSON
uv run python -c "import json; from clinicflow_api.main import app; print(json.dumps(app.openapi(), indent=2, ensure_ascii=False))" > docs/openapi.json

# 2. El segundo comando: Consultar la estructura de la respuesta con jq
jq '.paths["/doctors"].get.responses["200"].content["application/json"].schema' docs/openapi.json
```

## Bulk, Ruff, Pytest

```bash
uv run ruff check --fix . && uv run ruff format .
uv run python scripts/seed_bulk.py --doctors 0 --patients 0 --extra 'Urología:25'
uv run python scripts/seed_bulk.py --doctors 0 --patients 0 --extra 'Urología:25'   # no duplica

uv run python scripts/seed_bulk.py --doctors 0 --patients 0 --extra 'Oncología:45'
uv run python scripts/seed_bulk.py --doctors 0 --patients 0 --extra 'Urología:25' --extra 'Oncología:45'

#
uv run ruff check . && uv run ruff format --check . && uv run pytest -q

# verificar doctores elimnados
podman exec clinicflow-db-box psql -U krs -d clinicflow_db -c \
"SELECT d.last_name, d.first_name, d.license_number, s.name AS especialidad, d.is_active, d.deleted_at
 FROM doctors d JOIN specialties s ON s.id = d.specialty_id
 WHERE d.deleted_at IS NOT NULL
 ORDER BY d.deleted_at DESC;"

# solo contarlos
podman exec clinicflow-db-box psql -U krs -d clinicflow_db -c \
"SELECT count(*) AS eliminados FROM doctors WHERE deleted_at IS NOT NULL;"

# Y si prefieres salida vertical (una columna por línea), añade -x después de psql:
podman exec clinicflow-db-box psql -U krs -d clinicflow_db -x -c \
"SELECT * FROM doctors WHERE deleted_at IS NOT NULL;"

podman exec clinicflow-db-box psql -U krs -d clinicflow_db -c \
"SELECT s.name, count(d.id) AS doctores
 FROM specialties s LEFT JOIN doctors d ON d.specialty_id = s.id
 WHERE s.name IN ('Urologia','Urología') GROUP BY s.name;"

```