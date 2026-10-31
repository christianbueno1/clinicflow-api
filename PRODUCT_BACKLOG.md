# ClinicFlow — Product Backlog

> Estado: **v0.1** (2026-10-01). Solo épicas e historias de usuario de alto nivel, derivadas de `PRD.md` y `ROADMAP.md`. El desglose de tareas técnicas vive en `SPRINT_BACKLOG.md` y la tarea activa en `SPRINT_TASK.md`.

Leyenda de estado: **Hecho** · **En curso** · **Por hacer** · **Por confirmar**.

---

## E-01 — Cimientos del proyecto

> Bloque A del roadmap: base técnica para poder desarrollar y verificar la API.

| Campo | Detalle |
|---|---|
| Estado | Hecho (fases 1–4) |
| Referencias | `ROADMAP.md` fases 1–4 |

**HU-01 — Entorno de desarrollo reproducible**

- *Descripción:* Como desarrollador, quiero un proyecto base con configuración, `.env` y scripts de BD para poder levantar el entorno local sin pasos adivinados.
- *Criterio de aceptación:* `uv run fastapi dev` responde en `/health` y `/docs`; la app falla con mensaje claro si falta una variable; `setup-db.sh` deja PostgreSQL accesible y es repetible.
- *Estado:* Hecho
- *Referencias:* Fases 1–2, RF-12 implícito en RNF-05

**HU-02 — Base de datos local con Podman**

- *Descripción:* Como desarrollador, quiero scripts `setup`/`teardown` que gestionen red, pod, volumen y contenedor de PostgreSQL para poder resetear el entorno cuando lo necesite.
- *Criterio de aceptación:* `setup` deja PostgreSQL accesible; `teardown` lo limpia; ambos son repetibles y parametrizados con variables.
- *Estado:* Hecho
- *Referencias:* Fase 3, RNF-05

**HU-03 — Conexión asíncrona a la base de datos**

- *Descripción:* Como desarrollador, quiero engine, sesión y dependencia de sesión async para que los endpoints trabajen con la BD de forma no bloqueante.
- *Criterio de aceptación:* existe `/health/db` que consulta la base y responde; la sesión se inyecta con `Depends`.
- *Estado:* Hecho
- *Referencias:* Fase 4, `TECH-STACK.md` §2–3

---

## E-02 — Gestión de pacientes (CRUD)

> Primera entidad del dominio, de punta a punta.

**HU-04 — Definir el modelo `Patient`**

- *Descripción:* Como desarrollador, quiero un modelo SQLAlchemy de Paciente con sus restricciones y normalización para tener la base del dominio.
- *Criterio de aceptación:* tabla `patients` con columnas, unicidad global de cédula y correo, `deleted_at`, `naming_convention`, `sex` StrEnum M/F, cédula `String(10)`, `eager_defaults`.
- *Estado:* En curso (fase 5)
- *Referencias:* RF-01..RF-04 (persistencia), `SPECIFICATIONS.md` §3

**HU-05 — Migraciones con Alembic**

- *Descripción:* Como desarrollador, quiero Alembic con plantilla async para crear/evolucionar el esquema de forma controlada.
- *Criterio de aceptación:* `alembic upgrade head` crea la tabla y `downgrade` la elimina; la URL se toma de `Settings` en `env.py`.
- *Estado:* Por hacer (fase 6)
- *Referencias:* `TECH-STACK.md` §3, `SPECIFICATIONS.md` §6

**HU-06 — Crear paciente (`POST /api/v1/patients`)**

- *Descripción:* Como consumidor de la API, quiero registrar un paciente para disponer de sus datos.
- *Criterio de aceptación:* 201 con el recurso creado; validación previa; 409 ante duplicados; 422 ante datos inválidos; no persiste si la validación falla.
- *Estado:* Por hacer (fases 7–9)
- *Referencias:* RF-01, `SPECIFICATIONS.md` §4–5

**HU-07 — Consultar pacientes (`GET` por id y listado)**

- *Descripción:* Como consumidor de la API, quiero consultar un paciente por id y el listado paginado con filtros para encontrar registros.
- *Criterio de aceptación:* 200 con datos del registro; 404 si no existe o está borrado lógicamente; listado con `limit`/`offset` (20/100/0) y filtros de nombre, email, cédula, teléfono, sexo y edad.
- *Estado:* Por hacer (fases 8–10)
- *Referencias:* RF-02, `SPECIFICATIONS.md` §5

**HU-08 — Actualizar paciente (`PATCH`)**

- *Descripción:* Como consumidor de la API, quiero modificar parcialmente un paciente existente.
- *Criterio de aceptación:* PATCH parcial; `email`/`address` aceptan `null` para limpiar; cédula solo lectura; 404/409/422 según corresponda.
- *Estado:* Por hacer (fase 10)
- *Referencias:* RF-03, `SPECIFICATIONS.md` §4–5

**HU-09 — Eliminar paciente (borrado lógico)**

- *Descripción:* Como consumidor de la API, quiero eliminar un paciente sin perder la traza.
- *Criterio de aceptación:* DELETE fija `deleted_at` y responde 204; el registro deja de aparecer en listado y detalle; 404 si no existe.
- *Estado:* Por hacer (fase 10)
- *Referencias:* RF-04, `SPECIFICATIONS.md` §3–5

---

## E-03 — Reglas de dominio y calidad de API

**HU-10 — Validar datos de entrada**

- *Descripción:* Como consumidor de la API, quiero que las entradas inválidas se rechacen con errores claros.
- *Criterio de aceptación:* cédula `^\d{10}$`, sexo M/F, fecha de nacimiento no futura, normalización de correo/cédula; 422 ante violaciones.
- *Estado:* Por hacer (fase 7)
- *Referencias:* RF-05, `SPECIFICATIONS.md` §3–4

**HU-11 — Manejo de errores consistente**

- *Descripción:* Como consumidor de la API, quiero respuestas de error homogéneas y predecibles.
- *Criterio de aceptación:* `{ "detail": "..." }`; 404 distinto de 409 y de 422; el 409 cubre choques con pacientes borrados.
- *Estado:* Por hacer (fase 11)
- *Referencias:* RF-06, `SPECIFICATIONS.md` §5

**HU-12 — Documentación de la API**

- *Descripción:* Como consumidor de la API, quiero documentación interactiva alineada con la implementación.
- *Criterio de aceptación:* endpoints documentados con parámetros, cuerpos y respuestas (incluidos errores), disponibles en `/docs`.
- *Estado:* Por hacer (al cerrar las fases 9–11)
- *Referencias:* RF-07

**HU-13 — Datos de ejemplo**

- *Descripción:* Como desarrollador, quiero un script con datos simulados de Dr. House para probar la API.
- *Criterio de aceptación:* un comando carga pacientes que cumplen las reglas (cédula de 10 dígitos, sexo M/F).
- *Estado:* Por hacer (fase 12)
- *Referencias:* `PRD.md` §9.2

---

## E-04 — Verificación y calidad continua

**HU-14 — Pruebas de la funcionalidad**

- *Descripción:* Como desarrollador, quiero pruebas unitarias y de integración reproducibles para cada funcionalidad.
- *Criterio de aceptación:* suite con `pytest` + `pytest-asyncio`; integración contra BD de prueba en Podman; cobertura ≥ 80%.
- *Estado:* Por hacer (fases 13–14)
- *Referencias:* RF-08, `SPECIFICATIONS.md` §7, `TECH-STACK.md` §5

**HU-15 — Linter, tipos y hooks de git**

- *Descripción:* Como desarrollador, quiero que el commit se bloquee si el código no pasa las verificaciones.
- *Criterio de aceptación:* `ruff` (lint+format) y `mypy` pasan; hooks de git activos.
- *Estado:* Por hacer (fase 15)
- *Referencias:* `TECH-STACK.md` §5

**HU-16 — CI**

- *Descripción:* Como desarrollador, quiero que cada push ejecute pruebas y verificaciones.
- *Criterio de aceptación:* pipeline que corre pytest, ruff y mypy en cada push.
- *Estado:* Por hacer (fase 16)
- *Referencias:* `TECH-STACK.md` §5

---

## E-05 — Ampliación futura (sin compromiso)

- Entidad **Médico**, repitiendo el patrón.
- Entidad **Cita**, con relaciones entre entidades.
- Seguridad: autenticación, roles, límites de tasa.
- Observabilidad y rendimiento.
- Despliegue y pruebas de carga.

> Referencias: `ROADMAP.md` Bloque D, `PRD.md` §5.2.
