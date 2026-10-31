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
```

## Database

```bash
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c '\dt'
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -c '\d patients'
# para imprimar en vertical
podman exec -it clinicflow-db-box psql -U krs -d clinicflow_db -x -c 'select * from patients;'

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

