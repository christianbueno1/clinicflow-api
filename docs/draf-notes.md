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