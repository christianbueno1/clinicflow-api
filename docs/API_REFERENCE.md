# ClinicFlow API: referencia

Contrato de la API REST para quien construya el frontend. Documentación interactiva: `/docs` (Swagger) y `/openapi.json` (esquema para generar clientes).

## Convenciones

- **Base URL (desarrollo):** `http://127.0.0.1:8000`
- **Formato:** JSON (`Content-Type: application/json`).
- **IDs:** UUID v4 en texto.
- **Fechas y horas:** ISO 8601. Las citas se **envían con offset** (`2026-11-05T09:00:00-05:00`); un datetime sin zona horaria da 422. Las respuestas de citas vienen en UTC (`Z`); la disponibilidad viene con offset de la clínica. El cliente debe mostrar todo en `America/Guayaquil`.
- **Paginación:** `skip` (≥ 0, por defecto 0) y `limit` (1 a 100, por defecto 50). Aún no hay total de resultados.
- **PATCH:** actualización parcial; solo se envían los campos a cambiar.
- **CORS:** orígenes permitidos configurados en `CORS_ORIGINS` (JSON en `.env`).
- **Autenticación:** no implementada.

## Errores

| Código | Cuándo | Cuerpo |
|---|---|---|
| 404 | El recurso no existe (o está eliminado) | `{"detail": "mensaje"}` |
| 409 | Choca con una regla de negocio | `{"detail": "mensaje"}` |
| 422 | Validación del cuerpo o parámetros | `{"detail": [{"type", "loc", "msg", "input"}, ...]}` |

Los 404 y 409 devuelven `detail` como **texto** y el 422 como **lista**; el cliente debe manejar ambos formatos. Los mensajes están en español.

## Salud

| Método | Ruta | Respuesta |
|---|---|---|
| GET | `/health` | `{"status": "ok"}` |
| GET | `/health/db` | `{"status": "ok", "database": "connected", "result": 1}` |

## Especialidades

| Método | Ruta | Descripción | Éxito |
|---|---|---|---|
| POST | `/specialties` | Crear | 201 |
| GET | `/specialties` | Listar (por nombre) | 200 |
| GET | `/specialties/{id}` | Detalle | 200 |
| PATCH | `/specialties/{id}` | Editar | 200 |
| DELETE | `/specialties/{id}` | Eliminar (definitivo) | 204 |

Campos: `name` (2 a 100 caracteres, único). Respuesta: `{id, name}`.
Errores: 409 si el nombre ya existe; 409 al eliminar si tiene doctores.

## Doctores

| Método | Ruta | Descripción | Éxito |
|---|---|---|---|
| POST | `/doctors` | Crear | 201 |
| GET | `/doctors` | Listar. Filtros: `specialty_id`, `is_active` | 200 |
| GET | `/doctors/{id}` | Detalle | 200 |
| PATCH | `/doctors/{id}` | Editar | 200 |
| DELETE | `/doctors/{id}` | Eliminar (soft delete) | 204 |
| GET | `/doctors/{id}/availability` | Huecos del día | 200 |

Campos de entrada: `first_name`, `last_name` (1 a 100), `identification_number` (cédula ecuatoriana válida, única), `license_number` (1 a 50, único), `specialty_id`, `is_active` (por defecto `true`).
Respuesta: los campos anteriores, `specialty: {id, name}`, `created_at`, `updated_at`.
Errores: 404 si la especialidad no existe; 409 por cédula o licencia duplicada, o al eliminar con citas programadas a futuro. Un doctor eliminado deja de aparecer, pero su cédula y licencia siguen ocupadas.

### Disponibilidad

`GET /doctors/{id}/availability?date=2026-11-05&slot_minutes=30`

- `date` es obligatorio (`YYYY-MM-DD`). `slot_minutes`: 5 a 240, por defecto 30.
- Devuelve **todos** los huecos del horario de la clínica (por defecto 08:00 a 17:00, configurable), cada uno con `available: true|false`. Los huecos ocupados por citas programadas o ya pasados salen como `false`.
- Respuesta: `{doctor_id, day, timezone, slot_minutes, slots: [{starts_at, ends_at, available}]}`.
- 409 si el doctor está inactivo.
- Es informativa, no reserva: al agendar, el `POST /appointments` puede responder 409 si otro usuario tomó el hueco.

## Pacientes

| Método | Ruta | Descripción | Éxito |
|---|---|---|---|
| POST | `/patients` | Crear | 201 |
| GET | `/patients` | Listar. Búsqueda `q` por nombre, apellido o cédula | 200 |
| GET | `/patients/{id}` | Detalle | 200 |
| PATCH | `/patients/{id}` | Editar | 200 |
| DELETE | `/patients/{id}` | Eliminar (soft delete) | 204 |

Campos: `first_name`, `last_name` (1 a 100), `date_of_birth` (no futura), `sex` (`male` o `female`), `phone` (7 a 20 dígitos, espacios y `+` inicial opcional), `identification_number` (cédula válida, única), `email` (opcional, único, se guarda en minúsculas), `address` (opcional, máx. 500).
En PATCH, `email` y `address` aceptan `null` para borrarlos; en los demás campos, `null` se ignora.
Errores: 409 por cédula o email duplicado, o al eliminar con citas programadas a futuro.

## Citas

| Método | Ruta | Descripción | Éxito |
|---|---|---|---|
| POST | `/appointments` | Agendar | 201 |
| GET | `/appointments` | Listar. Filtros: `patient_id`, `doctor_id`, `status`, `date_from`, `date_to` | 200 |
| GET | `/appointments/{id}` | Detalle | 200 |
| PATCH | `/appointments/{id}` | Reprogramar o cambiar el motivo | 200 |
| PATCH | `/appointments/{id}/status` | Cambiar estado | 200 |

No hay DELETE: una cita se cancela.

Entrada (POST): `patient_id`, `doctor_id`, `starts_at` (con zona horaria, futura), `duration_minutes` (5 a 480, por defecto 30), `reason` (opcional, máx. 255). El servidor calcula `ends_at`.
Entrada (PATCH): `starts_at`, `duration_minutes`, `reason`. Solo las citas `scheduled` se pueden modificar.
Respuesta: `{id, patient_id, doctor_id, starts_at, ends_at, reason, status, created_at, updated_at}`.
En `date_from` y `date_to` usa `Z` en vez de `+` en el offset, porque en una URL el `+` se interpreta como espacio.

**Estados:** `scheduled` → `completed` | `cancelled` | `no_show`. Los estados finales no admiten cambios.

**Errores:**

- 404: paciente o doctor inexistente.
- 409: doctor inactivo; el doctor ya tiene una cita en ese horario; el paciente ya tiene una cita en ese horario; transición de estado no permitida; modificar una cita que no está `scheduled`.
- 422: fecha en el pasado o sin zona horaria.

Las citas consecutivas están permitidas (una termina a las 09:45 y otra empieza a las 09:45). Cancelar libera el horario.

## Generar el cliente tipado

```bash
npx @hey-api/openapi-ts -i http://127.0.0.1:8000/openapi.json -o src/app/api
```