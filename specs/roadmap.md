# ClinicFlow — Roadmap

> Estado: **borrador v0.1** (2026-09-29). Orden de implementación a alto nivel, en fases de **1–2 horas**.
> Ritmo de referencia: 5 h/día, unas 2–3 fases por día. Los detalles de cada fase se definen al empezarla.
>
> Cada fase termina con su criterio de "hecho". Antes de empezar una fase que toque un framework, se
> revisan sus novedades (ver `tech-stack.md`, sección 7).

## Bloque A — Cimientos

| # | Fase | Hecho cuando |
|---|---|---|
| 1 | Proyecto base: `uv init`, estructura de carpetas, `.gitignore`, `.env.example`, endpoint `/health` | `uv run fastapi dev` responde en `/health` y `/docs` |
| 2 | Configuración: lectura tipada de variables desde `.env` | La app falla con mensaje claro si falta una variable requerida |
| 3 | Base de datos en Podman: scripts `setup` y `teardown` (red, pod, volumen, PostgreSQL) con variables | `setup` deja PostgreSQL accesible; `teardown` lo limpia; ambos son repetibles |
| 4 | Conexión async: engine, sesión y dependencia de sesión | Un endpoint de prueba consulta la base y responde |

## Bloque B — Primera entidad: Paciente, de punta a punta

| # | Fase | Hecho cuando |
|---|---|---|
| 5 | Modelo SQLAlchemy de Paciente y convenciones de nombres | El modelo existe y está documentado en la guía |
| 6 | Alembic (plantilla async) y primera migración | `upgrade` crea la tabla y `downgrade` la elimina |
| 7 | Esquemas Pydantic (crear, actualizar, leer) con validaciones | Datos inválidos se rechazan con error 422 claro |
| 8 | Capa de acceso a datos y lógica (según la arquitectura elegida): crear y obtener por id | Funciona sin pasar por HTTP |
| 9 | Endpoints `POST` y `GET` por id | Se crea y consulta un paciente desde `/docs` |
| 10 | Endpoints de listado, actualización y borrado | CRUD completo funcionando desde `/docs` |
| 11 | Manejo de errores consistente (404, 409, 422) y códigos de estado | Todos los errores comparten el mismo formato |
| 12 | Datos de ejemplo (personajes y casos de *Dr. House*) con script de carga | Un comando deja la base con datos simulados |

## Bloque C — Calidad (se introduce ahora, no antes)

| # | Fase | Hecho cuando |
|---|---|---|
| 13 | Base de pruebas y pruebas unitarias | Las pruebas unitarias corren con un solo comando |
| 14 | Pruebas de integración contra una base de prueba en Podman | Cubren el CRUD completo de Paciente |
| 15 | Linter, formateo, verificación de tipos y hooks de git | El commit se bloquea si no pasan |
| 16 | CI | Cada push ejecuta pruebas y verificaciones |

## Bloque D — Ampliación (abierto, orden por decidir)

Candidatas, sin orden ni compromiso:

- Entidad **Médico**, repitiendo el patrón para validar que la guía de convenciones funciona.
- Entidad **Cita**, con relaciones entre entidades.
- Seguridad: autenticación, roles, límites de tasa.
- Observabilidad y rendimiento (tras la explicación pendiente).
- Despliegue y pruebas de carga.

## Cierre de cada fase

Cada fase actualiza la guía de convenciones y/o el registro de decisiones *(por confirmar)*.

## Pendientes que afectan al roadmap

- Arquitectura y patrones a practicar (define las fases 5, 8 y 9).
- Campos del Paciente, borrado físico o lógico, y paginación (definen las fases 5, 7 y 10).
- Herramientas de calidad y CI (definen los bloques C).
